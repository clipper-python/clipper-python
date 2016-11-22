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

def structure_factors ( mapin="", resol=8.0, callback=callbacks.interactive_flush ) :

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

    # nothing in, nothing out
    if mapin == "" :
        return log_string,xml_root,None
    
    # read the cryoEM map
    map_file.open_read ( mapin )
    map_file.import_nxmap_double ( nxmap )
    map_file.close_read()
    log_string += "\n  >> file %s has been read" % mapin
    callback( log_string, xml_root )
    original_cell = map_file.cell()

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

    # create HKL_info using user-supplied resolution parameter
    sg = clipper.Spacegroup.p1()
    resolution = clipper.Resolution(resol)
    hkl_info = clipper.HKL_info (sg, new_xmap.cell(), resolution, True )

    # fft the map
    f_phi = clipper.HKL_data_F_phi_float( hkl_info, new_xmap.cell() )
    log_string += "\n  >> now computing structure factors to %0.1f A resolution..." % resol
    callback( log_string, xml_root )
    new_xmap.fft_to ( f_phi )
    log_string += "\n  >> writing structure factors to MTZ file..."
    callback( log_string, xml_root )

    # setup an MTZ file so we can export our map coefficients
    mtzout  = clipper.CCP4MTZfile()
    mtzout.open_write ( "mapout_zero.mtz" )
    mtzout.export_hkl_info ( f_phi.hkl_info() )
    mtzout.export_hkl_data ( f_phi, "*/*/[F, PHI]" )
    mtzout.close_write()
    log_string += "\n  >> all done"
    callback( log_string, xml_root )

    return log_string,xml_root,f_phi
