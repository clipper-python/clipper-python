import sys
import numpy
import clipper

i = clipper.HKL_reference_index()

xmap = clipper.Xmap_float()
f = clipper.CCP4MAPfile()
f.open_read(sys.argv[1])
f.import_xmap_float(xmap)
f.close_read()

sg,samp,cell =  f.spacegroup(),f.grid_sampling(), f.cell()

print sg.symbol_laue()
print sg.symbol_hall()
print cell
print cell.dim, cell.angles

print cell.format()
print type(cell.format())

print samp.nu(),samp.nv(),samp.nw()

at = clipper.Atom()
# Do not know why this is necessary.
#at.element = clipper.String("H")
foo = clipper.String("foo")
at.element = "H"
print at.element
print dir(at.element)
print type(at.element)
print type(foo)

at.element = at.element

stats = clipper.Map_stats(xmap)
print stats.mean(), stats.min(),stats.max(),stats.std_dev()

# Range is unwrapped memory leak, but Range<double> and Range<float> are OK, but require specialized methods.
# There may be a better way, but this works!
print stats.range().max()
print stats.range().min()
print 0 in stats.range()
print 100 in stats.range()

c1 = clipper.Coord_orth(1,2,3)
c2 = clipper.Coord_orth(10,10,10)

c = c1+c2
cm = -c

print c.xyz
print cm.xyz

cif = clipper.CIFfile()
mydata = clipper.HKL_info()

fphi1 = clipper.HKL_data_F_phi_float(mydata)
fphi2 = clipper.HKL_data_F_phi_float(mydata)

fphi3 = fphi1 + fphi2*.5
fphi3p = fphi1 + .5*fphi2

if len(sys.argv)>2:
  cif.open_read (sys.argv[2])
  cif.import_hkl_info(mydata)
  print dir(mydata)
  sg,cell =  mydata.spacegroup, mydata.cell
  print sg.symbol_laue()
  print sg.symbol_hall()
  print cell
  print cell.dim, cell.angles
  myfsigf = clipper.HKL_data_F_sigF_float(mydata)
  status = clipper.HKL_data_Flag(mydata)
  cif.import_hkl_data(myfsigf)
  cif.import_hkl_data(status)
  cif.close_read()
  """
  # This is numpy testing
  print "F_SIGF size",myfsigf.data_size(), len(myfsigf)
  fsigf_numpy = numpy.zeros((myfsigf.data_size()* len(myfsigf)),numpy.float)
  print fsigf_numpy ; sys.stdout.flush()
  myfsigf.getDataNumpy(fsigf_numpy);
  print fsigf_numpy ; sys.stdout.flush()
  print fsigf_numpy+fsigf_numpy ; sys.stdout.flush()
  """
  print  mydata.num_reflections()
  cxtl = clipper.MTZcrystal()
  fm = clipper.MMDBfile()
  fm.read_file(sys.argv[3])
  mmol = clipper.MiniMol ()
  fm.import_minimol ( mmol )
  atoms = mmol.atom_list()
  print len(atoms)
  fc = clipper.HKL_data_F_phi_float( mydata, cxtl )
  sfcb = clipper.SFcalc_obs_bulk_float()
  print (fc, myfsigf, atoms)
  sfcb(fc, myfsigf, atoms)
  bulkfrc = sfcb.bulk_frac();
  bulkscl = sfcb.bulk_scale();
  print "Calculated structure factors ",bulkfrc,bulkscl
  fb = clipper.HKL_data_F_phi_float(mydata, cxtl)
  fd = clipper.HKL_data_F_phi_float(mydata, cxtl)
  phiw = clipper.HKL_data_Phi_fom_float(mydata, cxtl)
  flag = clipper.HKL_data_Flag(mydata, cxtl)
  freeflag = 1
  print flag,dir(flag), flag.num_obs(),flag.data_size()
  # Unfortunately, this is horribly slow. A much better way is required.
  """
  for ih in range(len(flag)):
    if ( not myfsigf[ih].missing()) and (status[ih].missing() or status[ih].flag()==freeflag):
      flag[ih].set_flag(clipper.SFweight_spline_float.BOTH)
    else:
      flag[ih].set_flag(clipper.SFweight_spline_float.NONE)
  """
  # Cheat(?) by putting some C++ into clipper.i
  clipper.SetFlagBothIfMissing(flag,myfsigf,status,freeflag)

  n_refln = 1000;
  n_param = 20;
  sfw = clipper.SFweight_spline_float( n_refln, n_param );
  fl = sfw( fb, fd, phiw, myfsigf, fc, flag );
  print "Done sigmaa calc"

  abcd = clipper.HKL_data_ABCD_float( mydata );
  print dir(abcd)
  abcd.compute_from_phi_fom( phiw );
  print "Done ABCD calc..."
 
  phiw.compute_from_abcd ( abcd );
  print "...and back to Phi_fom" 

  xmap2 = clipper.Xmap_float()
  rate = 1.33333
  gs = clipper.Grid_sampling(mydata.spacegroup, mydata.cell, mydata.resolution, rate)
  xmap2.init(mydata.spacegroup, mydata.cell, gs);
  print dir(xmap2)
  xmap2.fft_from( fb );
  stats2 = clipper.Map_stats(xmap2)
  print stats2.mean(), stats2.min(),stats2.max(),stats2.std_dev()
  if len(sys.argv)>4:
    fout = clipper.CCP4MAPfile()
    fout.open_write(sys.argv[4])
    fout.export_xmap_float(xmap2)
    fout.close_write()

  print "Do origin match"
  shift = clipper.Coord_frac()
  om = clipper.OriginMatch_float()
  invert = om(shift,fb,fd)
  print invert

  print shift.uvw




