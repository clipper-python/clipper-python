#
#  Copyright 2017 Jon Agirre & The University of York
#  Developed at York Structural Biology Laboratory - Cowtan group
#  Distributed under the terms of the LGPL (www.fsf.org)
#
#  Package containing functions for cutting density out of cryoEM maps

import clipper
from clipper_tools import callbacks
from lxml import etree


def cut_by_model ( mapin = "",
                   pdbin = "",
                   ipradius = 1.5,
                   ipresol  = 8.0,
                   ipbfact  = 0.0,
                   callback = callbacks.interactive_flush ) :

    #nxmap = clipper.NXmap_double( )
    xmap  = clipper.Xmap_double ( )
    sg = clipper.Spacegroup.p1()
    resolution = clipper.Resolution ( ipresol )

    # create log string so console-based apps get some feedback
    log_string = "\n  >> clipper_tools: em.cut_density.cut_by_model"
    log_string += "\n    mapin: %s" % mapin
    log_string += "\n    pdbin: %s" % pdbin
    log_string += "\n    bfact: %s" % ipbfact
    log_string += "\n    resol: %s" % ipresol
    log_string += "\n    radius: %s" % ipradius

    # create XML tree, to be merged in a global structured results file
    xml_root = etree.Element('program')
    xml_root.attrib['name']  = 'cut_by_model'
    xml_root.attrib['mapin'] = mapin
    xml_root.attrib['pdbin'] = pdbin
    xml_root.attrib['b_factor'] = str(ipbfact)
    xml_root.attrib['resolution'] = str(ipresol)
    xml_root.attrib['mask_radius'] = str(ipradius)
    callback( log_string, xml_root  )

    # nothing in, nothing out
    if mapin == "" or pdbin == "" :
        return log_string,xml_root,None

    # read the input atomic model
    from clipper_tools.io.molecules import read_pdb
    log_string_sub,xml_sub,mmol = read_pdb ( pdbin )
    log_string += log_string_sub
    xml_root.append ( xml_sub )
    
    callback( log_string, xml_root )

    # read the cryoEM map into xmap to get cell dimensions, etc.
    from clipper_tools.io.maps import read_xmap
    log_sub, xml_sub, xmap = read_xmap ( mapin )

    log_string += log_sub
    xml_root.append ( xml_sub )
    callback( log_string, xml_root )
    
    grid_sampling = clipper.Grid_sampling ( xmap.grid_asu().nu(),
                                            xmap.grid_asu().nv(),
                                            xmap.grid_asu().nw() )

    log_string += "\n  >> cell parameters: %s" % xmap.cell().format()
    callback( log_string, xml_root )

    # put map content in a numpy data structure
    import numpy
    map_numpy = numpy.zeros( (xmap.grid_asu().nu(), xmap.grid_asu().nv(), xmap.grid_asu().nw()), dtype='double')
    log_string += "\n  >> exporting a numpy array of %i x %i x %i grid points" \
               % (xmap.grid_asu().nu(), xmap.grid_asu().nv(), xmap.grid_asu().nw())
    data_points = xmap.export_numpy ( map_numpy )
    callback( log_string, xml_root  )

    atom_list = mmol.model().atom_list()

    mask = clipper.Xmap_float ( xmap.spacegroup(), xmap.cell(), grid_sampling )
        
    masker = clipper.EDcalc_mask_float ( ipradius )
    masker.compute ( mask, atom_list )

    mask_matrix = numpy.zeros( (xmap.grid_asu().nu(), xmap.grid_asu().nv(), xmap.grid_asu().nw()), dtype='double')
    mask_points = mask.export_numpy ( mask_matrix )

    log_string += "\n  >> the original map has %i points and the computed mask has %i points" % (data_points, mask_points)
    callback ( log_string, xml_root )

    masked_array = map_numpy * mask_matrix

    log_string += "\n  >> non-zero values: original= %i ; mask=%i ; product=%i" % (numpy.count_nonzero(map_numpy), numpy.count_nonzero(mask_matrix), numpy.count_nonzero(masked_array))

    xmap.import_numpy ( masked_array )

    # create HKL_info using user-supplied resolution parameter
    hkl_info = clipper.HKL_info (xmap.spacegroup(), xmap.cell(), resolution, True )

    # fft the map
    f_phi = clipper.HKL_data_F_phi_float( hkl_info, xmap.cell() )
    log_string += "\n  >> now computing map coefficients to %0.1f A resolution..." % ipresol
    callback( log_string, xml_root )
    
    xmap.fft_to ( f_phi )
    log_string += "\n  >> writing map coefficients to MTZ file mapout_cut_density.mtz"
    callback( log_string, xml_root )

    if ipbfact != 0.0 :
        f_phi.compute_scale_u_iso_fphi ( 1.0, clipper.Util.b2u(-ipbfact), f_phi )
        log_string += "\n  >> and applying B factor correction - using %3.2f\n" % ipbfact

    # setup an MTZ file so we can export our map coefficients
    from clipper_tools.io.map_coefficients import write_to_mtz
    log_sub,xml_sub = write_to_mtz ( f_phi, "mapout_cut_density.mtz" )

    log_string += log_sub
    xml_root.append ( xml_sub )

    log_string += "\n  >> all done"
    callback( log_string, xml_root )

    from clipper_tools.callbacks import offline_flush
    offline_flush ( log_string, xml_root )

if __name__ == '__main__':
    import sys
    print sys.argv
    if len(sys.argv) == 6 :
        cut_by_model ( sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]) )
    elif len(sys.argv) == 3 :
        cut_by_model ( sys.argv[1], sys.argv[2] )
    else :
        print "\n  >> clipper_tools: em.cut_density.cut_by_model"
        print "\n  >>    Parameters: mapin pdbin [radius] [resol] [bfact]\n\n"






