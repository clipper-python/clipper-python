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

    def test_orth_frac(self, verbose=False):
        '''
        Test minimol clipper-python bindings
        '''
        pdb_in_path = os.path.join(self.test_data_path, '1uoy.pdb')
        assert os.path.exists(pdb_in_path)
        # Set minimol
        f = clipper.MMDBfile()
        f.read_file(pdb_in_path)
        mmol = clipper.MiniMol()
        f.import_minimol(mmol)

        atoms = mmol.atom_list()

        cell = mmol.cell()
        frac_matrix = cell.matrix_frac()
        orth_matrix = cell.matrix_orth()

        self.assertAlmostEqual(orth_matrix[0][0], 43.615, places=3)
        self.assertAlmostEqual(orth_matrix[1][1], 58.436, places=3)
        self.assertAlmostEqual(orth_matrix[2][2], 53.415, places=3)
        self.assertAlmostEqual(frac_matrix[0][0], 0.02293, places=3)
        self.assertAlmostEqual(frac_matrix[1][1], 0.01711, places=3)
        self.assertAlmostEqual(frac_matrix[2][2], 0.01872, places=3)

        for at in atoms:
            c = at.coord_orth()
            cnew = orth_matrix * (frac_matrix * c)
            cdiff = cnew - c
            xdiff,ydiff,zdiff = cdiff.x(), cdiff.y(), cdiff.z()
            self.assertAlmostEqual(xdiff, 0.0, places=4)
            self.assertAlmostEqual(ydiff, 0.0, places=4)
            self.assertAlmostEqual(zdiff, 0.0, places=4)

        new_cell = clipper.Cell(clipper.Cell_descr(cell.a()+.2,cell.b(),cell.c(),cell.alpha(),cell.beta(),cell.gamma()))
        orth_matrix = new_cell.matrix_orth()

        self.assertAlmostEqual(orth_matrix[0][0], 43.815, places=3)
        self.assertAlmostEqual(orth_matrix[1][1], 58.436, places=3)
        self.assertAlmostEqual(orth_matrix[2][2], 53.415, places=3)
        for at in atoms:
            c = at.coord_orth()
            cnew = orth_matrix * (frac_matrix * c)
            cdiff = cnew - c
            xdiff,ydiff,zdiff = cdiff.x(), cdiff.y(), cdiff.z()
            self.assertTrue(abs(xdiff)<0.2)
            self.assertAlmostEqual(ydiff, 0.0, places=4)
            self.assertAlmostEqual(zdiff, 0.0, places=4)

if __name__ == '__main__':
    unittest.main()
