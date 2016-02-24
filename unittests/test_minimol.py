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

    def test_minimol(self, verbose=False):
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

        # Test PDB/cif i/o
        pdb_out_path = os.path.join(self.test_output, '1uoy_mm.pdb')
        cif_out_path = os.path.join(self.test_output, '1uoy_mm.cif')
        f.write_file(pdb_out_path, 0)
        assert os.path.exists(pdb_out_path)
        f.write_file(cif_out_path, clipper.MMDBManager.CIF)
        assert os.path.exists(cif_out_path)

        # What you get...
        if verbose:
            print dir(f)
            print dir(mmol)

        # Get atoms
        atoms = mmol.atom_list()
        if verbose:
            print dir(atoms)
            print atoms[0].coord_orth().x()
            print len(atoms)

        # Loop through atoms
        self.assertEqual(len(atoms), 581)
        if verbose:
            for i in range(len(atoms)):
                print atoms[i]

        # Get atom coords
        self.assertEqual(atoms[0].coord_orth().x(), -1.975)
        if verbose:
            for at in atoms:
                c = at.coord_orth()
                print c.x(), c.y(), c.z()

        # Loop through model, chain, residue, atom
        mod = mmol.model()
        for poly in mod:
            for mono in poly:
                for atom in mono:
                    if verbose:
                        print (atom.coord_orth().x(),
                               atom.coord_orth().y(),
                               atom.coord_orth().z())

        # Access atom directly, set properties
        self.assertEqual(mmol[0][0][0].occupancy(), 1.0)
        mmol[0][0][0].set_occupancy(0.5)
        print mmol[0][0][0].occupancy()
        self.assertEqual(mmol[0][0][0].occupancy(), 0.5)

        mmol[0][0][0].set_u_iso(10.0)
        print mmol[0][0][0].u_iso()
        self.assertEqual(mmol[0][0][0].u_iso(), 10.0)

if __name__ == '__main__':
    unittest.main()
