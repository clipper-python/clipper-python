import sys
import clipper

import unittest
import os
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
        Test CCP4MAPfile clipper-python bindings
        '''
        map_in_path = os.path.join(self.test_data_path, '4x1v_best.map')
        assert os.path.exists(map_in_path)
        xmap = clipper.Xmap_float()
        f = clipper.CCP4MAPfile()
        f.open_read(map_in_path)
        f.import_xmap_float(xmap)
        f.close_read()
        sg,samp,cell =  f.spacegroup(),f.grid_sampling(), f.cell()
        self.assertEquals(sg.symbol_hall(),"P 4cw")
        self.assertEquals(sg.symbol_hm(),"P 43")
        self.assertEquals(samp.nu(),90)
        self.assertEquals(samp.nv(),90)
        self.assertEquals(samp.nw(),64)
        stats = clipper.Map_stats(xmap)
        self.assertAlmostEquals(stats.mean(),0,places=7)
        self.assertAlmostEquals(stats.min(),-0.771,places=3)
        self.assertAlmostEquals(stats.max(),4.557,places=3)
        self.assertAlmostEquals(stats.std_dev(),0.385,places=3)
