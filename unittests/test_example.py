import unittest
import sys
import os
import shutil


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
        temporary test data producing during unit test.
        '''
        self.test_data = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test_data')
        self.test_output = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test_output')
        if not os.path.exists(self.test_output):
            os.makedirs(self.test_output)

    def tearDown(self):
        '''
        Always run at end of test, e.g. to remove temporary data.
        '''
        shutil.rmtree(self.test_output)

    def test_name(self):
        '''
        Example of unit test.  Tests should be as fast as possible (i.e. total
        time less than 1min) and test all main classes and functions of module
        in question.
        '''
        # Below prints test function name
        print '\n', sys._getframe().f_code.co_name
        # Below is an example set of assertions.  Please use something similar
        # to test expected output test module.  Unittest module has a wide
        # selection of assert functions, see above documentation for more.
        a = 1
        self.assertEqual(a, 1)
        a_dict = {1: 'foo', 2: 'bar'}
        b_dict = {1: 'foo', 2: 'bar'}
        self.assertDictEqual(a_dict, b_dict)
        self.assertDictContainsSubset({1: 'foo'}, a_dict)
        s = 'foo'
        self.assertMultiLineEqual(s, 'foo')
        f = 1.23456789
        self.assertAlmostEqual(f, 1.2345, places=3)

if __name__ == '__main__':
    unittest.main()
