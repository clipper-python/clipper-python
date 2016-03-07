import clipper


def read_pdb ( pdbin = "undefined" ) :

    log_string = "\n\t## clipper-utils: read_pdb \n\n"
    log_string += "\tpdbin: %s\n\n" % pdbin

    xml_root = etree.Element('read_pdb')

    if pdbin is not "undefined" :

        f = clipper.MMDBfile()
        f.read_file ( pdbin )

        log_string += "\tFile opened and read\n"

        mmol = clipper.MiniMol ()
        f.import_minimol ( mmol )
        
        log_string += "\tMiniMol imported\n"
        
        log_string += "\n\t## \n\n"
        
        return log_string, xml_root, mmol
    
    else :
        log_string += "\tNo input PDB was supplied\n"
        return log_string, xml_root, None
