"""
Clipper app to perform ffts and map stats
Copyright 2003-2004 Kevin Cowtan & University of York all rights reserved

Python port, Stuart McNicholas, 2015.
"""

"""
THIS EXAMPLE IS NOT YET COMPLETE!! A way needs to be found of doing cpu 
intensive loops, which are currently commented out, in C++. This has to be
done in some kind of general way, ideally.

However, all the necessary clipper classes for everything else should be
wrapped and running this script with an MTZ file should be possible. Crashes
likely.
"""


import sys
import clipper

# defaults
title = ""
ipfile = "NONE";
ipcolf = "NONE";
ipcold = "NONE";
ipcola = "NONE";
ipcolh = "NONE";
opfile = "patterson.map";
adiff = False;
oremv = False;
limit_e = 1.0e20;
weight_e = 0.0;
reso = clipper.Resolution()
grid = clipper.Grid_sampling()
nprm = 12;

for arg in range(len(sys.argv)):
    if ( sys.argv[arg] == "-title" ):
      arg += 1
      title = sys.argv[arg];
    elif ( sys.argv[arg] == "-mtzin" ):
      arg += 1
      ipfile = sys.argv[arg];
    elif ( sys.argv[arg] == "-mapout" ):
      arg += 1
      opfile = sys.argv[arg];
    elif ( sys.argv[arg] == "-colin-fo" ):
      arg += 1
      ipcolf = sys.argv[arg];
    elif ( sys.argv[arg] == "-colin-fano" ):
      arg += 1
      ipcola = sys.argv[arg];
    elif ( sys.argv[arg] == "-colin-fdiff" ):
      arg += 1
      ipcold = sys.argv[arg];
    elif ( sys.argv[arg] == "-resolution" ):
      arg += 1
      reso = clipper.Resolution( float(sys.argv[arg]) );
    elif ( sys.argv[arg] == "-grid" ):
      arg += 1
      g = sys.argv[arg].split(",");
      grid = clipper.Grid_sampling( int(g[0]), int(g[1]), int(g[2]) );
    elif ( sys.argv[arg] == "-e-limit" ):
      arg += 1
      limit_e = float(sys.argv[arg])
    elif ( sys.argv[arg] == "-e-weight" ):
      arg += 1
      weight_e = float(sys.argv[arg])
    elif ( sys.argv[arg] == "-anomalous" ):
      adiff = True;
    elif ( sys.argv[arg] == "-origin-removal" ):
      oremv = True;

if len(sys.argv) <= 1:
    print "Usage: cpatterson\n\t-mtzin <filename>\n\t-mapout <filename>\n\t-colin-fo <colpath>\n\t-colin-fano <colpath>\n\t-colin-fdiff <colpath>\n\t-resolution <reso>\n\t-grid <nu>,<nv>,<nw>\n\t-e-limit <limit>\n\t-e-weight <weight>\n\t-anomalous\n\t-origin-removal\nCalculate Patterson from Fobs or Fano.\nFor E-Patterson <weight> = 1, for F-Patterson <weight> = 0, and other values.\n<limit> can reject reflections or differences by E-value.\n";
    sys.exit(1);

# make data objects
mtzin =  clipper.CCP4MTZfile()
cxtl =clipper.MTZcrystal()
hkls = clipper.HKL_info()
hklp = clipper.HKL_info()
#  typedef clipper::HKL_data_base::HKL_reference_index HRI; ??
mtzin.set_column_label_mode( clipper.CCP4MTZfile.Legacy );

# open file
mtzin.open_read( ipfile );
spgr = mtzin.spacegroup();

print spgr.symbol_hm()
cell = mtzin.cell();
print cell.a(),cell.b(),cell.c(),cell.alpha(),cell.beta(),cell.gamma()

if ( ipcolf != "NONE" ):
  mtzin.import_crystal( cxtl, ipcolf+".F_sigF.F" );
if ( ipcola != "NONE" ):
  mtzin.import_crystal( cxtl, ipcola+".F_sigF_ano.F+");
if ( not cxtl.is_null() ):
  cell = cxtl;
if ( reso.is_null() ):
  reso = mtzin.resolution();
hkls.init( spgr, cell, reso, True );
fsig = clipper.HKL_data_F_sigF_float(hkls)
dsig = clipper.HKL_data_F_sigF_float(hkls)
fano = clipper.HKL_data_F_sigF_ano_float(hkls)
if ( ipcolf != "NONE" ):
  mtzin.import_hkl_data( fsig, ipcolf );
if ( ipcola != "NONE" ):
  mtzin.import_hkl_data( fano, ipcola );
# cpatterson.cpp has ipcolf below. Surely that cannot be right?
print "ipcold",ipcold
if ( ipcold != "NONE" ):
  print "Importing",ipcold
  mtzin.import_hkl_data( dsig, ipcold );
mtzin.close_read();

# make mean/difference F if necessary
if ( ipcola != "NONE" ):
    if ( adiff ):
      fsig.compute_diff_from_fano( fano );
    else:
      fsig.compute_mean_from_fano( fano );

# FIXME - NEED TO SO SOMETHING CLEVER ABOUT THESE LOOPS!
if ( ipcold != "NONE" ) :
   clipper.SetData(fsig,dsig,"BOTH_PRESENT","1F=-2F","1F=ZERO")
"""
  // subtract difference F if necessary
  if ( ipcold != "NONE" ) 
    for ( HRI ih = fsig.first(); !ih.last(); ih.next() )
      if ( !fsig[ih].missing() && !dsig[ih].missing() )
	fsig[ih].f() -= dsig[ih].f();
      else
	fsig[ih].f() = 0.0;

"""
# calculate E scale factor
esig = clipper.HKL_data_E_sigE_float(hkls)
print esig
esig.compute_from_fsigf( fsig );

params_init = []
for i in range(nprm):
  params_init.append(1.0)
basis_fo = clipper.BasisFn_spline( esig, nprm, 2.0 );
print basis_fo
target_fo = clipper.TargetFn_scaleEsq_E_sigE(esig)
print target_fo
escale = clipper.ResolutionFn(hkls, basis_fo, target_fo, params_init)
print escale

"""
  // reject reflections by E-value
  for ( HRI ih = esig.first(); !ih.last(); ih.next() )
    if ( !esig[ih].missing() )
      if ( esig[ih].E() / sqrt( escale.f(ih) ) > limit_e )
	fsig[ih] = clipper::data32::F_sigF();

  // calculate E-F combination
  for ( HRI ih = fsig.first(); !ih.last(); ih.next() )
    if ( !fsig[ih].missing() )
      fsig[ih].scale( pow( escale.f(ih), 0.5*weight_e ) );

"""
# get Patterson spacegroup
print spgr
print spgr.generator_ops()
pspgr = clipper.Spacegroup( clipper.Spgr_descr( spgr.generator_ops().patterson_ops() ) );
hklp.init( pspgr, cell, reso, True );

# make patterson coeffs
fphi = clipper.HKL_data_F_phi_float( hklp );
"""
  for ( HRI ih = fphi.first(); !ih.last(); ih.next() ) {
    clipper::data32::F_sigF f = fsig[ih.hkl()];
    if ( !f.missing() ) {
      fphi[ih].f() = f.f()*f.f();
      fphi[ih].phi() = 0.0 ;
    }
  }

"""
# origin removal
if oremv:
  basis_fp = clipper.BasisFn_spline( fphi, nprm, 2.0 );
  print basis_fp
  target_fp = clipper.TargetFn_meanFnth_F_phi(fphi, 1.0)
  oscale = clipper.ResolutionFn( hklp, basis_fp, target_fp, params_init )
"""
    for ( HRI ih = fphi.first(); !ih.last(); ih.next() )
      if ( !fphi[ih].missing() )
	fphi[ih].f() -= oscale.f(ih);
"""

# make grid if necessary
if ( grid.is_null() ):
  grid.init( pspgr, cell, reso );

# make xmap
xmap = clipper.Xmap_float( pspgr, cell, grid );
xmap.fft_from_float( fphi );

# write map
mapout = clipper.CCP4MAPfile()
mapout.open_write(opfile)
mapout.export_xmap_float(xmap)
mapout.close_write()
