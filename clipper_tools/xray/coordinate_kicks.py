import clipper
from lxml import etree

def random_kicks ( mmol=None, amplitude=0.0, frequency=0.0 ) :

    log_string = "\n\t## clipper-utils: random_kicks \n\n"
    log_string += "\tamplitude: %f\n\n" % amplitude
    log_string += "\tfrequency: %f\n\n" % frequency

    xml_root = etree.Element('random_kicks')

    if mmol is None :
        log_string += "ERROR: no valid molecule object supplied\n\n"
        return log_string, xml_root

    if amplitude == 0.0 or frequency == 0.0 :
        log_string += "ERROR: cannot compute kicks with zero amplitude and/or frequency\n\n"
        return log_string, xml_root

    if frequency < 0.0 or frequency > 100.0 :
        log_string += "ERROR: frequency is not in the (0,100] range\n\n"
        return log_string, xml_root

    import random

    model = mmol.model()

    for chain in model :
        for residue in chain :
            for atom in residue :
                if random.uniform (0.0, 100.0) < frequency :
                    x = atom.coord_orth().x() + random.uniform ( 0.1, amplitude )
                    y = atom.coord_orth().y() + random.uniform ( 0.1, amplitude )
                    z = atom.coord_orth().z() + random.uniform ( 0.1, amplitude )
                    coords = clipper.Coord_orth(x,y,z)
                    atom.set_coord_orth ( coords )

    return log_string,xml_root,mmol