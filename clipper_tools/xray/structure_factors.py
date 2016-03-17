import clipper
from lxml import etree

def structure_factors ( fsigf=None, hklinfo=None, mmol=None, bulk_solvent=True ) :

    log_string = "\n  >> clipper_tools: structure_factors"
    log_string += "\n     bulk_solvent: %s" % bulk_solvent

    xml_root = etree.Element('structure_factors')
    xml_root.attrib['bulk_solvent'] = str(bulk_solvent)

    cxtl = clipper.MTZcrystal()
    atoms = mmol.atom_list()
    
    fc = clipper.HKL_data_F_phi_float( mydata, cxtl )
    
    sfcb = clipper.SFcalc_obs_bulk
    sfcb(fc, myfsigf, atoms)
    
    bulkfrc = sfcb.bulk_frac();
    bulkscl = sfcb.bulk_scale();

    etree.SubElement(xml_root, 'bulk_fraction').text = str bulkfrc
    etree.SubElement(xml_root, 'bulk_scale').text   = str bulkslc
    
    log_string += "\n    bulk_fraction: %f " % bulkfrc
    log_string += "\n    bulk_scale: %f " % bulkscl
    
    log_string += "\n  << structure_factors has finished\n"
    xml_root.attrib['ok']    = 'yes'

    
    return log_string, xml_root, fc
