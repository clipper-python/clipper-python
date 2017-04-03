#
#  Copyright 2017 Jon Agirre & The University of York
#  Developed at York Structural Biology Laboratory - Cowtan group
#  Distributed under the terms of the LGPL (www.fsf.org)
#
#  Package containing functions for reading and writing structure factors
#  to and from CCP4 MTZ files

import clipper
from lxml import etree


def read_from_mtz ( mtzin = "", colin = "F,SIGF" ) :
    """Reads reflection and sigmas, returns a HKL_data_F_sigF_float object
    
       Parameters:
         mtzin -- a string path to an MTZ file containing measured reflections
         colin -- configurable column name, defaults to F,SIGF, could also be DANO,SIGDANO
         callback -- a function that takes care of log string and xml flushing
       
       Returns:
         a plain text log string, an XML etree and a clipper.HKL_data_F_sigf object"""

    log_string = "\n  >> clipper_tools: io.structure_factors.read_from_mtz"
    log_string += "\n     mtzin: %s" % mtzin

    xml_root = etree.Element('input_file')
    xml_root.attrib['name'] = mtzin
    xml_root.attrib['type'] = 'mini MTZ'
    
    hkl_data = clipper.HKL_data_F_sigF_float()
    hkl_info = clipper.HKL_info ()
    
    if mtzin is not "" :
        mtzfilein = clipper.CCP4MTZfile()
        mtzfilein.open_read ( mtzin )
        mtzfilein.import_hkl_info (hkl_info, True)
        mtzfilein.import_hkl_data (hkl_data, "*/*/[" + colin + "]")
    else :
        return log_string, xml_root, hkl_data, hkl_info
    
    print (dir(hkl_data))
    
    log_string += "\n  << read_from_mtz has finished\n"
    xml_root.attrib['ok']    = 'yes'
    
    return log_string, xml_root, hkl_info, hkl_data



def write_to_mtz ( dataout = None, mtzout = "" ) :

    log_string = "\n  >> clipper_tools: io.structure_factors.write_to_mtz"
    log_string += "\n     mtzout: %s" % mtzout

    xml_root = etree.Element('output_file')
    xml_root.attrib['name'] = mtzout
    xml_root.attrib['type'] = 'mini MTZ'
    
    if dataout is not None and mtzout is not "" :
        mtzfileout  = clipper.CCP4MTZfile()
        mtzfileout.open_write ( mtzout )
        mtzfileout.export_hkl_info ( dataout.hkl_info() )
        mtzfileout.export_hkl_data ( dataout, "*/*/[F, PHI]" )
        mtzfileout.close_write()
        
        xml_root.attrib['ok'] = "yes"
    
    else :
        xml_root.attrib['ok'] = "no"

    log_string += "\n  << write_to_mtz has finished\n"
    
    return log_string, xml_root