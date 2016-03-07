import clipper
from lxml import etree


def read_xmap ( mapin = "undefined" ) :

    log_string = "\n\t## clipper-utils: read_xmap \n\n"
    log_string += "\tmapin: %s\n\n" % mapin

    xml_root = etree.Element('read_xmap')

    if mapin is not "undefined" :

        map_file = clipper.CCP4MAPfile()
        map_file.open_read ( map_name )
        map_data = clipper.Xmap_float()
        map_file.import_xmap_float ( map_data )
        map_file.close_read()

        return log_string, xml_root, map_file



def read_nxmap ( mapin = "undefined" ) :

    log_string = "\n\t## clipper-utils: read_nxmap \n\n"
    log_string += "\tmapin: %s\n\n" % mapin

    xml_root = etree.Element('read_nxmap')

    if mapin is not "undefined" :

        map_file = clipper.CCP4MAPfile()
        map_file.open_read ( map_name )
        map_data = clipper.NXmap_float()
        map_file.import_nxmap_float ( map_data )
        map_file.close_read()

        return log_string, xml_root, map_file

