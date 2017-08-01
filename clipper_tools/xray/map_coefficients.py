import clipper
from lxml import etree

## Computes sigmaa map coefficients
#  @param fsig a clipper.HKL_data_F_sigF_float object
#  @param hklinfo a clipper.HKL_info object
#  @param mmol a clipper.MiniMol object
#  @param bulk_solvent boolean parameter, set True for turning bulk solvent correction on
#  @return a plain text log string, an XML etree and a clipper.HKL_data_F_phi_float object

