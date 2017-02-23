import clipper
from lxml import etree

# to be finished (jon.agirre@york.ac.uk)
def read_from_mtz ( mtzin = "" ) :
    
    log_string = "\n  >> clipper_tools: io.map_coefficients.read_from_mtz"
    log_string += "\n     mtzin: %s" % mtzin

    xml_root = etree.Element('input_file')
    xml_root.attrib['name'] = mtzin
    xml_root.attrib['type'] = 'mini MTZ'
    log_string += "\n  << read_from_mtz has finished\n"
    xml_root.attrib['ok']    = 'yes'
    
    return log_string, xml_root



def write_to_mtz ( dataout = None, mtzout = "" ) :

    log_string = "\n  >> clipper_tools: io.map_coefficients.write_to_mtz"
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