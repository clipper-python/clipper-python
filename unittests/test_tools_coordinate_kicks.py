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

    def test_tools_coordinate_kicks(self, verbose=False):
        '''
        Test tools_coordinate_kicks
        '''
        pdb_input = os.path.join(self.test_data_path, '4x1v.pdb')
        pdb_output = os.path.join(self.test_data_path, '4x1v_fragment_kicked.pdb')
        
        assert os.path.exists(pdb_input)
        
        # read pdb, kick coordinates, write pdb
        from clipper_tools.io.molecules import read_pdb, write_pdb
        from clipper_tools.xray.coordinate_kicks import fragment_kicks
        
        log_string,xml_root,mmol = read_pdb(pdb_input)
        log_string,xml_root      = fragment_kicks(mmol, 5, 20, 40.0)
        log_string,xml_root      = write_pdb(pdb_output)

        assert os.path.exists(pdb_output)
        
if __name__ == '__main__':
    unittest.main()
