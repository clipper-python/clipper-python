#
#     Copyright (C) 2015 CCP-EM
#
#     This code is distributed under the terms and conditions of the
#     CCP-EM Program Suite Licence Agreement as a CCP-EM Application.
#     A copy of the CCP-EM licence can be obtained by writing to the
#     CCP-EM Secretary, RAL Laboratory, Harwell, OX11 0FA, UK.
#

import clipper
import numpy
import numpy as np
import os
import matplotlib.pyplot as plt


class ClipperMTZ(object):
    def __init__(self,
                 mtz_in_path=None):
        self.mtz = clipper.CCP4MTZfile()
        self.hkl_info = clipper.HKL_info()
        self.mtz_in_path = mtz_in_path
        if self.mtz_in_path is not None:
            assert os.path.exists(self.mtz_in_path)
        self.spacegroup = None
        self.cell = None
        self.column_data = {}

    def import_column_data(self, column_label, get_resolution=True):
        if self.mtz_in_path is not None:
            self.mtz.open_read(self.mtz_in_path)
            self.mtz.import_hkl_info(self.hkl_info)
            self.spacegroup = self.hkl_info.spacegroup()
            self.cell = self.hkl_info.cell()
            fsigf = clipper.HKL_data_F_phi_float(self.hkl_info)
            self.mtz.import_hkl_data(fsigf, '/*/*/' + column_label)
            self.mtz.close_read()
            # Convert to numpy
            fsigf_numpy = numpy.zeros((fsigf.data_size() * len(fsigf)),
                                      numpy.float)
            fsigf.getDataNumpy(fsigf_numpy)
            # Reshape and transpose
            fsigf_numpy = numpy.reshape(fsigf_numpy, (-1, 2))
            fsigf_numpy = numpy.transpose(fsigf_numpy)
            # Convert to rec array to store col names
            names = [n for n in fsigf.data_names().split()]
            fsigf_numpy = np.core.records.fromarrays(
                fsigf_numpy,
                names=names,
                formats='float64, float64')
            # Append to dictionary
            self.column_data[column_label] = fsigf_numpy
            # Get resolution column
            if get_resolution:
                res_numpy = numpy.zeros(fsigf_numpy.shape[0])
                for n in xrange(fsigf_numpy.shape[0]):
                    r = self.hkl_info.invresolsq(n)
                    res_numpy[n] = r
                self.column_data['resolution_1/Ang^2'] = res_numpy

