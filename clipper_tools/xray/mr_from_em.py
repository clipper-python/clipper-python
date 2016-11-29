#
#  Copyright 2016 Jon Agirre & The University of York
#  Distributed under the terms of the LGPL (www.fsf.org)
#
#  Package containing functions for making it easy to do MR with cryoEM maps
#  To do: account for errors in the scale using control point refinement

import clipper
from clipper_tools import callbacks
from lxml import etree

## Reads EM map, sets origin to 0 and computes structure factors
#  @param mapin string path to a map that will be read into a clipper.NXmap_float object
#  @param resol estimated resolution (float)
#  @return a plain text log string, an XML etree and a clipper.HKL_data_F_phi_float object

def structure_factors ( mapin="", resol=8.0, fast_extent_determination=True, callback=callbacks.interactive_flush ) :

    ## Reads numpy array, determines the extent of the electron density
    #  @param numpy_in a numpy array containing grid points
    #  @param tolerance number of points in a plane with value greater than 1 sigma
    #  @return a vector of grid indices: (min_u, max_u, min_v, max_v, min_w, max_w)

    def determine_extent (  numpy_in, tolerance ) :
    
        log_string = ""
        min = clipper.Coord_orth()
        max = clipper.Coord_orth()
        
        map_mean = numpy.mean(map_numpy)
        map_std  = numpy.std (map_numpy)
        
        mask = map_numpy > map_mean + map_std
        
        sum_u = sum(sum(mask))
        sum_w = sum(sum(numpy.transpose(mask)))
        sum_v = sum(numpy.transpose(sum(mask)))
        
        log_string += "\n  >> dumping 1D summaries of the map's content:\n\n  >> U:\n %s\n" % sum_u
        log_string += "\n  >> V:\n %s\n" % sum_v
        log_string += "\n  >> W:\n %s\n" % sum_w
        
        point_list = [ ]
    
        for idx_u, val_u in enumerate(sum_u) :
            if val_u > tolerance :
                point_list.append ( idx_u )

        min_u = point_list[0]
        max_u = point_list[-1]
        
        log_string += "\n  >> First meaningful U: %i ; Last meaningful U: %i" \
              % (min_u, max_u)

        point_list = [ ]
    
        for idx_v, val_v in enumerate(sum_v) :
            if val_v > tolerance :
                point_list.append ( idx_v )

        min_v = point_list[0]
        max_v = point_list[-1]

        log_string += "\n  >> First meaningful V: %i ; Last meaningful V: %i" \
              % (min_v, max_v)

        point_list = [ ]
    
        for idx_w, val_w in enumerate(sum_w) :
            if val_w > tolerance :
                point_list.append ( idx_w )

        min_w = point_list[0]
        max_w = point_list[-1]

        log_string += "\n  >> First meaningful W: %i ; Last meaningful W: %i\n" \
              % (min_w, max_w)

        extent = [ min_u, max_u, min_v, max_v, min_w, max_w ]
        
        return extent, log_string


    # create log string so console-based apps get some feedback
    log_string = "\n  >> clipper_tools: mr_from_em.structure_factors"
    log_string += "\n            mapin: %s" % mapin
    log_string += "\n            resol: %s" % resol

    # create XML tree, to be merged in a global structured results file
    xml_root = etree.Element('structure_factors')
    xml_root.attrib['mapin'] = mapin
    xml_root.attrib['resol'] = str ( resol )
    callback( log_string, xml_root  )

    nxmap = clipper.NXmap_double( )
    map_file = clipper.CCP4MAPfile( )
    sg = clipper.Spacegroup.p1()

    # nothing in, nothing out
    if mapin == "" :
        return log_string,xml_root,None
    
    # read the cryoEM map
    map_file.open_read ( mapin )
    map_file.import_nxmap_double ( nxmap )
    map_file.close_read()
    log_string += "\n  >> file %s has been read" % mapin
    callback( log_string, xml_root )

    # get the grid in a local variable for efficiency
    grid = nxmap.grid()

    # get map content in a numpy data structure
    import numpy
    map_numpy = numpy.zeros( (nxmap.grid().nu(), nxmap.grid().nv(), nxmap.grid().nw()), dtype='double')
    log_string += "\n  >> exporting a numpy array of %i x %i x %i grid points" \
               % (nxmap.grid().nu(), nxmap.grid().nv(), nxmap.grid().nw())
    callback( log_string, xml_root  )

    # export data to numpy
    data_points = nxmap.export_numpy ( map_numpy )
    log_string += "\n  >> %i data points have been exported" % data_points
    callback ( log_string, xml_root )
    rtop_zero = clipper.RTop_double(nxmap.operator_orth_grid().rot())
    log_string += "\n  >> moving origin..."
    log_string += "\n     original translation: %s  new origin: %s" % (nxmap.operator_orth_grid().trn(), rtop_zero.trn())
    callback( log_string, xml_root )

    # create new map with origin in zero and import numpy array
    nxmap_zero = clipper.NXmap_double(nxmap.grid(), rtop_zero )
    data_points = nxmap_zero.import_numpy ( map_numpy )
    log_string += "\n  >> %i data points have been imported from numpy" % data_points
    callback( log_string, xml_root )

    # dump map to disk
    map_file.open_write ( "mapout_zero.mrc" )
    map_file.export_nxmap_double ( nxmap_zero )
    map_file.close_write()
    log_string += "\n  >> map file written to disk"
    callback( log_string, xml_root )

    # read it back to an xmap so we can fft-it
    new_xmap = clipper.Xmap_double ()
    map_file.open_read ( "mapout_zero.mrc" )
    map_file.import_xmap_double ( new_xmap )
    map_file.close_read()

    # compute the extent
    extent, temp_log = determine_extent ( map_numpy, 20 )
    log_string += temp_log
    extent_list = [ extent[1] - extent[0], extent[3] - extent[2], extent[5] - extent[4] ]
    max_extent = max(extent_list)

    callback ( log_string, xml_root )

    large_a = ( new_xmap.cell().a() * ( max_extent + new_xmap.grid_asu().nu())) / new_xmap.grid_asu().nu()
    large_b = ( new_xmap.cell().b() * ( max_extent + new_xmap.grid_asu().nv())) / new_xmap.grid_asu().nv()
    large_c = ( new_xmap.cell().c() * ( max_extent + new_xmap.grid_asu().nw())) / new_xmap.grid_asu().nw()

    cell_desc = clipper.Cell_descr ( large_a, large_b, large_c, \
                  new_xmap.cell().alpha(), new_xmap.cell().beta(), new_xmap.cell().gamma() )

    large_p1_cell = clipper.Cell ( cell_desc )
    large_grid_sampling = clipper.Grid_sampling ( max_extent + new_xmap.grid_asu().nu(),\
                                                  max_extent + new_xmap.grid_asu().nv(),\
                                                  max_extent + new_xmap.grid_asu().nw() )

    large_xmap = clipper.Xmap_double ( sg, large_p1_cell, large_grid_sampling )

    log_string += "\n  >> new grid: nu=%i nv=%i nw=%i" % (large_xmap.grid_asu().nu(), \
                                                          large_xmap.grid_asu().nv(), \
                                                          large_xmap.grid_asu().nw() )

    log_string += "\n  >> putting map into a large p1 cell..."
    log_string += "\n  >> new cell parameters: %s" % large_p1_cell.format()
    callback( log_string, xml_root )

    large_xmap.import_numpy ( map_numpy )

    # create HKL_info using user-supplied resolution parameter
    resolution = clipper.Resolution ( resol )
    hkl_info = clipper.HKL_info (sg, large_p1_cell, resolution, True )

    # fft the map
    f_phi = clipper.HKL_data_F_phi_float( hkl_info, large_p1_cell )
    log_string += "\n  >> now computing map coefficients to %0.1f A resolution..." % resol
    callback( log_string, xml_root )
    large_xmap.fft_to ( f_phi )
    log_string += "\n  >> writing coefficients to MTZ file..."
    callback( log_string, xml_root )

    # setup an MTZ file so we can export our map coefficients
    mtzout  = clipper.CCP4MTZfile()
    mtzout.open_write ( "mapout_zero_padded.mtz" )
    mtzout.export_hkl_info ( f_phi.hkl_info() )
    mtzout.export_hkl_data ( f_phi, "*/*/[F, PHI]" )
    mtzout.close_write()
    log_string += "\n  >> all done"
    callback( log_string, xml_root )


    return log_string,xml_root,f_phi

    def subroutine ( ) :
        return

