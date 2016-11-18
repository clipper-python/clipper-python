#
#  Copyright 2016 Jon Agirre & The University of York
#  Distributed under the terms of the LGPL (www.fsf.org)
#
#  Package containing functions for making it easy to do MR with cryoEM maps
#  To do: account for errors in the scale using control point refinement

import clipper
from lxml import etree

## Reads EM map, sets origin to 0 and computes structure factors
#  @param mapin string path to a map that will be read into a clipper.NXmap_float object
#  @param resol estimated resolution (float)
#  @return a plain text log string, an XML etree and a clipper.HKL_data_F_phi_float object

def structure_factors ( mapin="", resol=8.0 ) :

    log_string = "\n  >> clipper_tools: mr_from_em.structure_factors"
    log_string += "\n            mapin: %s" % mapin
    log_string += "\n            resol: %s" % resol

    xml_root = etree.Element('structure_factors')
    xml_root.attrib['mapin'] = mapin
    xml_root.attrib['resol'] = str ( resol )

    nxmap = clipper.NXmap_float( )
    map_file = clipper.CCP4MAPfile( )
    
    if mapin == "" :
        return log_string,xml_root,None
    
    map_file.open_read ( mapin )
    map_file.import_nxmap_float ( nxmap )
    map_file.close_read()
    cell = map_file.cell()

    grid = nxmap.grid()

    map_file.open_write ( "nxmap_no_numpy.mrc" )
    map_file.export_nxmap_float ( nxmap )
    map_file.set_cell(cell)
    map_file.close_write()

    print grid.format()
    print cell.format()

    rtop = clipper.rtop_float()
    print dir(rtop)
    rtop = nxmap.operator_orth_grid()
    print rtop.format()

    origin = clipper.vec3_float(0.0,0.0,0.0)
    rtop_zero_origin = clipper.rtop_float ( rtop.rot() )

    import numpy

    map_numpy = numpy.zeros( (nxmap.grid().nu(), nxmap.grid().nv(), nxmap.grid().nw()), dtype='double')
    nxmap.export_numpy ( map_numpy )
    nxmap.import_numpy ( map_numpy )

    map_file.open_write ( "nxmap_numpy.mrc" )
    map_file.export_nxmap_float ( nxmap )
    map_file.set_cell(cell)
    map_file.close_write()

    return log_string,xml_root,nxmap
