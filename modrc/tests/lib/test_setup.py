import pathlib
import tempfile
import unittest

from modrc.lib import setup


class TestInitialSetup(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.parent_dir = pathlib.Path(self.temp.name)

    def tearDown(self):
        # destroy the temp directory
        self.temp.cleanup()

    def test_modrc_directory_already_exists(self):
        """Test that exception is raised if the ModRC directory already exists."""
        modrc_dir = self.parent_dir.joinpath('.modrc')
        modrc_dir.mkdir()
        with self.assertRaises(FileExistsError):
            setup.initial_setup(self.parent_dir)

    def test_initial_setup(self):
        """Test ModRC directory creation."""
        modrc_dir = setup.initial_setup(self.parent_dir)
        self.assertEqual(modrc_dir.name, '.modrc')
        self.assertTrue(modrc_dir.exists())

    def test_create_modrc_file(self):
        """Test .modrc file creation"""
        modrc_dir = setup.initial_setup(self.parent_dir)
        modrc_file = modrc_dir.joinpath('.modrc')
        self.assertTrue(modrc_file.exists())

    def test_create_packages_directory(self):
        """Test package directory creation."""
        modrc_dir = setup.initial_setup(self.parent_dir)
        packages_dir = modrc_dir.joinpath('packages')
        self.assertTrue(packages_dir.exists())

    def test_create_live_directory(self):
        """Test live directory creation."""
        modrc_dir = setup.initial_setup(self.parent_dir)
        live_dir = modrc_dir.joinpath('live')
        self.assertTrue(live_dir.exists())


# runner
if __name__ == '__main__':
    unittest.main()
