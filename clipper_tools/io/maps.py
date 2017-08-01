import clipper
from lxml import etree


def read_xmap ( mapin = "" ) :

    log_string =  "\n  >> clipper_tools: io.maps.read_xmap"
    log_string += "\n     mapin: %s" % mapin

    xml_root = etree.Element('input_file')

    if mapin is not "" :

        map_file = clipper.CCP4MAPfile()
        map_file.open_read ( mapin )
        map_data = clipper.Xmap_double()
        map_file.import_xmap_double ( map_data )
        map_file.close_read()
        
        log_string += "\n  << read_xmap has finished\n"
        
        xml_root.attrib['name'] = mapin
        xml_root.attrib['type'] = "xmap"
        xml_root.attrib['ok'] = "yes"
        return log_string, xml_root, map_data



def read_nxmap ( mapin = "" ) :

    log_string = "\n\t## clipper_tools: io.maps.read_nxmap"
    log_string += "\n\tmapin: %s" % mapin

    xml_root = etree.Element('input_file')

    if mapin is not "" :

        map_file = clipper.CCP4MAPfile()
        map_file.open_read ( mapin )
        map_data = clipper.NXmap_double()
        map_file.import_nxmap_double ( map_data )
        map_file.close_read()
        
        log_string += "\n  << read_xmap has finished\n"
        
        xml_root.attrib['name'] = mapin
        xml_root.attrib['type'] = "nxmap"
        xml_root.attrib['ok'] = "yes"
        return log_string, xml_root, map_data


def write_xmap ( datain = None, mapout = "" ) :
    
    log_string = "\n\t## clipper_tools: io.maps.write_xmap"
    log_string += "\n\tmapout: %s" % mapout

    xml_root = etree.Element('output_file')

    if mapout is not "" and datain is not None :

        map_file = clipper.CCP4MAPfile()
        map_file.open_write ( mapout )
        map_file.export_xmap_double ( datain )
        map_file.close_write()
        
        log_string += "\n  << write_xmap has finished\n"
        
        xml_root.attrib['name'] = mapout
        xml_root.attrib['type'] = "CCP4/MRC map file"
        xml_root.attrib['ok'] = "yes"
        return log_string, xml_root


def write_nxmap ( datain = None, mapout = "" ) :
    
    log_string = "\n\t## clipper_tools: io.maps.write_nxmap"
    log_string += "\n\tmapout: %s" % mapout

    xml_root = etree.Element('output_file')

    if mapout is not "" and datain is not None :

        map_file = clipper.CCP4MAPfile()
        map_file.open_write ( mapout )
        map_file.export_nxmap_double ( datain )
        map_file.close_write()
        
        log_string += "\n  << write_nxmap has finished\n"
        
        xml_root.attrib['name'] = mapout
        xml_root.attrib['type'] = "CCP4/MRC map file"
        xml_root.attrib['ok'] = "yes"
        return log_string, xml_root
