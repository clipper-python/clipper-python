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
                   ipradius = 2.5,
                   ipresol  = 1.0,
                   callback = callbacks.interactive_flush ) :

    nxmap = clipper.NXmap_double( )
    xmap  = clipper.Xmap_double ( )
    map_file = clipper.CCP4MAPfile( )
    sg = clipper.Spacegroup.p1()
    resolution = clipper.Resolution ( ipresol )

    # create log string so console-based apps get some feedback
    log_string = "\n  >> clipper_tools: em.cut_density.cut_from_model"
    log_string += "\n            mapin: %s" % mapin
    log_string += "\n            resol: %s" % ipresol

    # create XML tree, to be merged in a global structured results file
    xml_root = etree.Element('cut_by_model')
    xml_root.attrib['mapin'] = mapin
    xml_root.attrib['pdbin'] = pdbin
    callback( log_string, xml_root  )

    # nothing in, nothing out
    if mapin == "" or pdbin == "" :
        return log_string,xml_root,None

    # read the cryoEM map into nxmap, get map data irrespective of origin
    map_file.open_read ( mapin )
    map_file.import_nxmap_double ( nxmap )
    map_file.close_read()
    log_string += "\n  >> file %s has been read as nxmap" % mapin
    callback( log_string, xml_root )

    # read pdb, kick coordinates, write pdb
    from clipper_tools.io.molecules import read_pdb
    log_string_sub,xml_root,mmol = read_pdb ( pdbin )
    log_string += log_string_sub
    callback( log_string, xml_root )

    # read the cryoEM map into xmap to get cell dimensions, etc.
    map_file.open_read ( mapin )
    map_file.import_xmap_double ( xmap )
    map_file.close_read()
    log_string += "\n  >> file %s has been read as xmap" % mapin
    callback( log_string, xml_root )
    
    grid_sampling = clipper.Grid_sampling ( xmap.grid_asu().nu(),
                                                  xmap.grid_asu().nv(),
                                                  xmap.grid_asu().nw() )

    log_string += "\n  >> cell parameters: %s" % xmap.cell().format()
    log_string += "\n     original translation: %s" % nxmap.operator_orth_grid().trn()
    callback( log_string, xml_root )

    # put map content in a numpy data structure
    import numpy
    map_numpy = numpy.zeros( (nxmap.grid().nu(), nxmap.grid().nv(), nxmap.grid().nw()), dtype='double')
    log_string += "\n  >> exporting a numpy array of %i x %i x %i grid points" \
               % (nxmap.grid().nu(), nxmap.grid().nv(), nxmap.grid().nw())
    callback( log_string, xml_root  )

    atom_list = mmol.model().atom_list()

    mask = clipper.Xmap_float ( xmap.spacegroup(), xmap.cell(), grid_sampling )
        
    masker = clipper.EDcalc_mask_float ( ipradius )
    masker.compute ( mask, atom_list )

    # fft the map
    f_phi = clipper.HKL_data_F_phi_float( hkl_info, xmap.cell() )
    log_string += "\n  >> now computing map coefficients to %0.1f A resolution..." % resol
    callback( log_string, xml_root )
    
    new_xmap.fft_to ( f_phi )
    log_string += "\n  >> writing map coefficients to MTZ file mapout_cut_density.mtz"
    callback( log_string, xml_root )

    # setup an MTZ file so we can export our map coefficients
    mtzout  = clipper.CCP4MTZfile()
    mtzout.open_write ( "mapout_cut_density.mtz" )
    mtzout.export_hkl_info ( f_phi.hkl_info() )
    mtzout.export_hkl_data ( f_phi, "*/*/[F, PHI]" )
    mtzout.close_write()
    log_string += "\n  >> all done"
    callback( log_string, xml_root )


if __name__ == '__main__':
    import sys
    cut_by_model ( sys.argv[1], sys.argv[2] )







