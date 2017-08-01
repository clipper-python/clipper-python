from __future__ import print_function

import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),".."))
try:
    import clipper
except ImportError:
    print ('\n\nClipper module not found.'
           '\nPlease check you are calling ccp4-python and / or python path '
           'is set correctly.\n\n')
    sys.exit()


def main():
    '''
    Run all unit tests.
    All test scripts should be named with the prefix test_ and placed in :
    clipper-python/
    TestLoader().discover will automatically locate the tests and append to
    test suite.
    For example unit test script see:
    test_example.py
    '''

    # Check python version >= 2.7
    if sys.version_info < (2, 7):
        print ('\n\nError: please use python >= 2.7')
        print ('Current python version : ', str(
            sys.version_info.major) + '.' + str(sys.version_info.minor + '\n'))
        sys.exit()
    clipper_unittest_path = os.path.dirname(os.path.abspath(__file__))

    # XXX Temporay workaround
    # Normal procedure move up one directory to include all code.  For now only
    # run test code in this directory as some tests crash
    if False:
        start_dir = os.path.abspath(os.path.join(clipper_unittest_path, '..'))
    else:
        start_dir = clipper_unittest_path

    clipper_core_tests = unittest.TestLoader().discover(
        start_dir=start_dir,
        pattern='test_*')

    alltests = unittest.TestSuite((clipper_core_tests))
    allresults = unittest.TextTestRunner().run(alltests)

    # Results review
    print ('\n---- START OF TEST RESULTS')
    print (allresults)
    print ('\nallresults::errors')
    print (allresults.errors)
    print ('\nallresults::failures')
    print (allresults.failures)
    print ('\nallresults::skipped')
    print (allresults.skipped)
    print ('\nallresults::successful')
    print (allresults.wasSuccessful())
    print ('\nallresults::test-run')
    print (allresults.testsRun)
    print ('\n---- END OF TEST RESULTS')

if __name__ == '__main__':
    main()
