#
#     Copyright (C) 2015 CCP-EM
#
#     This code is distributed under the terms and conditions of the
#     CCP-EM Program Suite Licence Agreement as a CCP-EM Application.
#     A copy of the CCP-EM licence can be obtained by writing to the
#     CCP-EM Secretary, RAL Laboratory, Harwell, OX11 0FA, UK.
#

import unittest
import os
import shutil
from clipper_tools.em import structure_factors
import numpy


class Test(unittest.TestCase):
    '''
    Unit test for Molrep (invokes GUI).
    '''
    def setUp(self):
        '''
        Setup test data and output directories.
        '''
        self.test_data = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test_data')
        self.test_output = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test_output')

    def tearDown(self):
        '''
        Remove temporary data.
        '''
        if os.path.exists(path=self.test_output):
            shutil.rmtree(self.test_output)

    def test_em_stucture_factors(self):
        print 'Unit test: EM MTZ I/O'
        mtz_in_path = os.path.join(self.test_data,
                                   'starting_map.mtz')
        mtz = structure_factors.ClipperMTZ(mtz_in_path=mtz_in_path)
        column_label = '[Fout0, Pout0]'
        mtz.import_column_data(column_label=column_label)
        #
        assert mtz.cell.a() == 75.0
        assert len(mtz.column_data[column_label]['F']) == 32559
        self.assertAlmostEquals(
            mtz.column_data[column_label][1]['F'],
            27.050485611,
            places=6)
        self.assertAlmostEquals(
            mtz.column_data[column_label][1][0],
            27.050485611,
            places=6)
        self.assertAlmostEquals(
            mtz.column_data[column_label][23122]['F'],
            10.9580,
            places=3)
        self.assertAlmostEquals(
            numpy.degrees(mtz.column_data[column_label][23122]['phi']),
            81.8,
            places=1)
        f_max = numpy.nanmax(mtz.column_data[column_label]['F'])
        f_mean = numpy.nanmean(mtz.column_data[column_label]['F'])
        self.assertAlmostEquals(f_max,
                                2429.0,
                                places=1)
        self.assertAlmostEquals(f_mean,
                                36.40,
                                places=2)
        # Convert mtz to absolute
        phi_deg = numpy.degrees(
            numpy.absolute(mtz.column_data[column_label]['phi']))
        phi_max = numpy.nanmax(phi_deg)
        self.assertAlmostEquals(phi_max,
                                360.0,
                                places=1)
        phi_abs_mean = numpy.nanmean(phi_deg)
        self.assertAlmostEquals(phi_abs_mean,
                                180.20,
                                places=1)
        assert len(mtz.column_data['resolution_1/Ang^2']) ==\
            len(mtz.column_data[column_label]['phi'])


if __name__ == '__main__':
    unittest.main()
