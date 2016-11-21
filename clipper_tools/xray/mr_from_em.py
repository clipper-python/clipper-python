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

def structure_factors ( mapin="", resol=8.0, callback=callbacks.flush_log ) :

    # create log string so console-based apps get some feedback
    log_string = "\n  >> clipper_tools: mr_from_em.structure_factors"
    log_string += "\n            mapin: %s" % mapin
    log_string += "\n            resol: %s" % resol
    callbacks.flush_log ( log_string )

    # create XML tree, to be merged in a global structured results file
    xml_root = etree.Element('structure_factors')
    xml_root.attrib['mapin'] = mapin
    xml_root.attrib['resol'] = str ( resol )

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
    callbacks.flush_log ( log_string )
 
    # get the grid in a local variable for efficiency
    grid = nxmap.grid()

    # get map content in a numpy data structure
    import numpy
    map_numpy = numpy.zeros( (nxmap.grid().nu(), nxmap.grid().nv(), nxmap.grid().nw()), dtype='double')
    log_string += "\n  >> exporting a numpy array of %i x %i x %i grid points" \
               % (nxmap.grid().nu(), nxmap.grid().nv(), nxmap.grid().nw())
    callbacks.flush_log ( log_string )

    data_points = nxmap.export_numpy ( map_numpy )
    log_string += "\n  >> %i data points have been exported" % data_points

    rtop_zero = clipper.RTop_double(nxmap.operator_orth_grid().rot())
    log_string += "\n  >> moving origin..."
    log_string += "\n     original translation: %s  new origin: %s" % (nxmap.operator_orth_grid().trn(), rtop_zero.trn())

    nxmap_zero = clipper.NXmap_double(nxmap.grid(), rtop_zero )
    data_points = nxmap_zero.import_numpy ( map_numpy )
    log_string += "\n  >> %i data points have been imported from numpy" % data_points
    callbacks.flush_log ( log_string )
    
    map_file.open_write ( "nxmap_numpy.mrc" )
    map_file.export_nxmap_double ( nxmap_zero )
    map_file.close_write()
    log_string += "\n  >> Map file written to disk!"

    callbacks.flush_log ( log_string )

    return log_string,xml_root,nxmap
