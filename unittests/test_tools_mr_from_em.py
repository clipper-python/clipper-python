import unittest
import os
import shutil
import clipper
import test_data
import clipper
import clipper_tools
from clipper_tools.xray.mr_from_em import structure_factors


class Test(unittest.TestCase):

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

    def test_tools_mr_from_em(self, verbose=False):
        
        map_input = os.path.join(self.test_data_path, 'emd_3407.mrc')
        log, xml, fphi = structure_factors ( mapin=map_input, resol=3.3 )

if __name__ == '__main__':
    unittest.main()