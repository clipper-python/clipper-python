import clipper
from lxml import etree

def read_pdb ( pdbin = "undefined" ) :

    log_string = "\n  >> clipper_tools: read_pdb"
    log_string += "\n     pdbin: %s" % pdbin

    xml_root = etree.Element('read_pdb')

    if pdbin is not "undefined" :

        f = clipper.MMDBfile()
        f.read_file ( pdbin )
        mmol = clipper.MiniMol ()
        f.import_minimol ( mmol )
        
        log_string += "\n  << read_pdb has finished\n"
        
        return log_string, xml_root, mmol
    
    else :
        log_string += "\n  ERROR: No input PDB was supplied"
        return log_string, xml_root, None



def write_pdb ( pdbout = "xyzout.pdb", molout = None ) :

    log_string = "\n  >> clipper_tools: write_pdb"
    log_string += "\n     pdbout: %s" % pdbout

    xml_root = etree.Element('write_pdb')

    if molout is None :
        return log_string,xml_root
    else :
        mmdb = clipper.MMDBfile()
        mmdb.export_minimol( molout );
        mmdb.write_file( pdbout, 0 );
        log_string += "\n  << write_pdb has finished \n"

    return log_string,xml_root
