import sys
import clipper

f = clipper.MMDBfile()
f.read_file (sys.argv[1])
mmol = clipper.MiniMol ()
print mmol
f.import_minimol ( mmol )

atoms = mmol.atom_list()

cell = mmol.cell()
frac_matrix = cell.matrix_frac()
new_cell = clipper.Cell(clipper.Cell_descr(cell.a()+.2,cell.b(),cell.c(),cell.alpha(),cell.beta(),cell.gamma()))
orth_matrix = new_cell.matrix_orth()


for at in atoms:
  c = at.coord_orth()
  cnew = orth_matrix * (frac_matrix * c)
  cdiff = cnew - c
  print ("% 6.4f % 6.4f % 6.4f") % (cdiff.x(), cdiff.y(), cdiff.z())

