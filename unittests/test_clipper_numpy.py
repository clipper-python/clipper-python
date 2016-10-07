from __future__ import print_function
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),".."))
import clipper
import numpy

import unittest
import shutil
import clipper
import test_data


class Test(unittest.TestCase):
    '''
    Example test script.  For all python code please write a
    corresponding unit test in a similar format to this example.  The test
    script should be named test_<module_name>.py and placed in same source
    directory as the module it is testing.  For further information on unit
    tests please see:

    https://docs.python.org/2/library/unittest.html
    '''

    def setUp(self):
        '''
        Always run at start of test, e.g. for creating directory to store
        temporary test data producing during unit test
        '''
        self.test_data_path = os.path.dirname(test_data.__file__)
        assert os.path.exists(self.test_data_path)
        self.test_output = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test_output')
        if not os.path.exists(self.test_output):
            os.makedirs(self.test_output)

    def tearDown(self):
        '''
        Always run at end of test, e.g. to remove temporary data
        '''
        shutil.rmtree(self.test_output)

    def test_clipper_numpy(self, verbose=False):
        '''
        Test numpy clipper-python bindings and CIF reading.
        '''

        cif = clipper.CIFfile()
        mydata = clipper.HKL_info()
        cif_in_path = os.path.join(self.test_data_path, '4x1v.cif')
        assert os.path.exists(cif_in_path)
        cif.open_read (cif_in_path)
        cif.import_hkl_info(mydata)
        sg,cell =  mydata.spacegroup(), mydata.cell()
        self.assertAlmostEquals(cell.a(),44.59,places=3)
        self.assertAlmostEquals(cell.b(),44.59,places=3)
        self.assertAlmostEquals(cell.c(),32.94,places=3)
        self.assertAlmostEquals(cell.alpha(),1.570796,places=6)
        self.assertAlmostEquals(cell.beta(),1.570796,places=6)
        self.assertAlmostEquals(cell.gamma(),1.570796,places=6)
        myfsigf = clipper.HKL_data_F_sigF_float(mydata)
        status = clipper.HKL_data_Flag(mydata)
        cif.import_hkl_data(myfsigf)
        cif.import_hkl_data(status)
        cif.close_read()
        fsigf_numpy = numpy.zeros((myfsigf.data_size()* len(myfsigf)),numpy.float)
        myfsigf.getDataNumpy(fsigf_numpy);
        i = 0
        test_f_sig_f_data = [ 5.54820013046 , 1.37300002575 , 3.76679992676 , 1.04229998589 , 217.498001099 , 2.99740004539 , 4.34929990768 , 1.16820001602 , 5.93720006943 , 1.57710003853 , 3.85949993134 , 1.11129999161 , 157.050003052 , 2.50629997253 , 6.6061000824 , 2.30500006676 , 11.4969997406 , 2.55789995193 , 5.8341999054 , 1.54460000992 , 180.908996582 , 3.49650001526 , 6.76160001755 , 2.36299991608 , 7.12340021133 , 2.56310009956 , 5.70559978485 , 1.66779994965 , 80.7269973755 , 2.87069988251 , 8.69659996033 , 3.13499999046 , 15.4949998856 , 3.25819993019 , 111.319999695 , 1.08910000324 , 105.82900238 , 1.37000000477 , 193.830993652 , 1.60860002041 , 51.813999176 , 0.959100008011 , 102.278999329 , 1.15299999714 , 97.1070022583 , 1.23099994659 , 261.845001221 , 1.74699997902 , 156.783004761 , 1.9959000349 , 71.9779968262 , 1.62220001221 , 52.9140014648 , 1.18400001526 , 73.2170028687 , 1.23230004311 , 89.4909973145 , 1.25510001183 , 38.7389984131 , 1.13900005817 , 69.7870025635 , 1.2460000515 , 36.9379997253 , 1.25059998035 , 54.6240005493 , 1.60409998894 , 29.7430000305 , 1.81970000267 , 44.4739990234 , 1.54340004921 , 14.9239997864 , 1.64839994907 , 10.498000145 , 2.10789990425 , 62.6800003052 , 1.29030001163 , 152.975006104 , 1.29550004005 , 48.2270011902 , 0.990499973297 , 363.785003662 , 2.64770007133 , 9.69950008392 , 1.07669997215 , 98.0699996948 , 1.13880002499 , 42.6469993591 , 1.12839996815 , 174.261001587 , 1.52559995651 , 262.213989258 , 2.44720005989 ]
        j = 0
        f_list = []
        for i in range(20):
            n = fsigf_numpy[i]
            if not numpy.isnan(fsigf_numpy[i]):
                self.assertAlmostEquals(fsigf_numpy[i],
                                        test_f_sig_f_data[j],
                                        places=6)
                j += 1
            if i % 2 == 0:
                f_list.append(n)

        # N.B. getDataNumpy returns 1D array:
        #        [F, sigF, F, sigF...]
        # Convert to 2D array with columns F and sigF
        fsigf_numpy = numpy.reshape(fsigf_numpy, (-1, 2))
        fsigf_numpy = numpy.transpose(fsigf_numpy)
        print (fsigf_numpy.shape)
        for i in range(10):
            if not numpy.isnan(fsigf_numpy[0][i]):
                assert fsigf_numpy[0][i] == f_list[i]

if __name__ == '__main__':
    unittest.main()
