#
#  Copyright 2017 Jon Agirre & The University of York
#  Developed at York Structural Biology Laboratory - Cowtan group
#  Distributed under the terms of the LGPL (www.fsf.org)
#
#  Package containing functions for making it easy to do MR with cryoEM maps
#  To do: account for errors in the scale using control point refinement

import clipper
import numpy
from clipper_tools import callbacks
from lxml import etree


def calculate_map ( mtzin = "",
                    colin_fo = "F,SIGF",
                    colin_dano = "",
                    resol = None,
                    callback = callbacks.interactive_flush ) :
    """Reads EM map, sets origin to 0, pads cell and computes finely-sampled structure factors
    
       Parameters:
         mtzin -- a string path to an MTZ file containing measured amplitudes
         colin-fo -- configurable column name, defaults to F,SIGF
         colin-dano -- empty by default; if specified, patterson will be calculated on anomalous differences
         resol -- resolution cutoff (float)
         callback -- a function that takes care of log string and xml flushing
       
       Returns:
         a plain text log string, an XML etree and a clipper.HKL_data_F_phi_float object"""


    # create log string so console-based apps get some feedback
    log_string = "\n  >> clipper_tools: xray.patterson.calculate_map"
    log_string += "\n    mtzin: %s" % mtzin
    log_string += "\n    colin_fo: %s" % colin_fo
    log_string += "\n    colin_dano: %s" % colin_dano


    # create XML tree, to be merged in a global structured results file
    xml_root = etree.Element('structure_factors')
    xml_root.attrib['mtzin'] = mtzin
    xml_root.attrib['colin_fo'] = colin_fo
    xml_root.attrib['colin_dano'] = colin_dano

    from clipper_tools.io.structure_factors import read_from_mtz
    log_sub, xml_sub, hkl_info, hkl_data = read_from_mtz ( mtzin, colin_fo )

    if resol is not None :
        resolution_cutoff = clipper.Resolution(resol)
    else :
        resolution_cutoff = hkl_info.resolution()

    log_string += "\n    resol: %.2f" % ( resolution_cutoff.limit() )
    xml_root.attrib['resol'] = "%.2f" % ( resolution_cutoff.limit() )
    callback( log_string, xml_root  )

    p_spgr = clipper.Spacegroup ( clipper.Spgr_descr (hkl_info.spacegroup().generator_ops().patterson_ops()) )
    p_hklinfo = clipper.HKL_info ( p_spgr, hkl_info.cell(), resolution_cutoff, True )
    f_phi = clipper.HKL_data_F_phi_float (p_hklinfo) # map coefficients to be calculated later

    numpy_data = numpy.zeros ((hkl_data.data_size() * len ( hkl_data )), numpy.float)
    numpy_coef = numpy.zeros ((hkl_data.data_size() * len ( hkl_data )), numpy.float)

    print "data array size is %i" % (hkl_data.data_size() * len ( hkl_data ))

    n_data = hkl_data.export_numpy ( numpy_data )

    numpy_data = numpy_data.reshape ( ( -1, 2) ) # so we have column 0 = F, column 1 = SIGF
    print "len(f_phi)=%i   len(original_data)= %i    len(numpy_f_phi)=%i and n_data is %i" % (len(f_phi), len(hkl_data), len(numpy_data), n_data)
    print numpy_data



    numpy_data[:,1] = 0 # we are going to re-use the F,SIGF numpy array as F,PHI
                        # so we need to set PHI = 0 for the Patterson map

    numpy_data[:,0] = numpy.power ( numpy_data[:,0], 2 ) # square the amplitudes

    numpy_data = numpy_data.reshape ( -1 ) # need to put it back in a 1-D array for export
    f_phi.import_numpy ( numpy_data )

    from clipper_tools.io.map_coefficients import write_to_mtz
    log_sub, xml_sub = write_to_mtz ( f_phi, "patterson.mtz" )
    callback (log_string, xml_root )

    return

def peak_search ( ) :
    return

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 3 :
        calculate_map ( sys.argv[1], sys.argv[2] )
    else :
        print "\n  >> clipper_tools: xray.patterson"
        print "\n  >>    Parameters: mtzin [colin-fo] [colin-dano] [resol]\n\n"

