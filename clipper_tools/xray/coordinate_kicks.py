import clipper
from lxml import etree

def random_kicks ( mmol=None, amplitude=0.0, frequency=0.0 ) :

    log_string = "\n  >> clipper_tools: random_kicks"
    log_string += "\n     amplitude: %f" % amplitude
    log_string += "\n     frequency: %f" % frequency

    xml_root = etree.Element('random_kicks')
    xml_root.attrib['amplitude']    = str(amplitude)
    xml_root.attrib['frequency']    = str(frequency)

    if mmol is None :
        log_string += "ERROR: no valid molecule object supplied\n\n"
        xml_root.attrib['ok']    = 'no'
        return log_string, xml_root

    if amplitude == 0.0 or frequency == 0.0 :
        log_string += "ERROR: cannot compute kicks with zero amplitude and/or frequency\n\n"
        xml_root.attrib['ok']    = 'no'
        return log_string, xml_root

    if frequency < 0.0 or frequency > 100.0 :
        log_string += "ERROR: frequency is not in the (0,100] range\n\n"
        xml_root.attrib['ok']    = 'no'
        return log_string, xml_root

    import random

    model = mmol.model()

    kicked = not_kicked = 0

    for chain in model :
        for residue in chain :
            for atom in residue :
                if random.uniform (0.0, 100.0) < frequency :
                    sign = random.choice ( [-1, 1] )
                    x = atom.coord_orth().x() + sign * random.uniform ( 0.01, amplitude )
                    y = atom.coord_orth().y() + sign * random.uniform ( 0.01, amplitude )
                    z = atom.coord_orth().z() + sign * random.uniform ( 0.01, amplitude )
                    coords = clipper.Coord_orth(x,y,z)
                    atom.set_coord_orth ( coords )
                    kicked += 1
                else :
                    not_kicked += 1

    log_string += "\n     %i atoms have been kicked, while %i remain in their original positions" % (kicked, not_kicked )
    log_string += "\n     That means %f percent of the atoms have been kicked" % (kicked / (kicked + not_kicked) *100.0 )

    log_string += "\n  << random_kicks has finished\n"
    xml_root.attrib['ok']    = 'yes'

    return log_string,xml_root,mmol

