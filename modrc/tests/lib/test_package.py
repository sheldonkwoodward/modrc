import pathlib
import tempfile
import unittest

from modrc.lib import package, setup


class TestCreatePackage(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.parent_dir = pathlib.Path(self.temp.name)
        self.modrc_dir = setup.initial_setup(self.parent_dir)
        self.packages_dir = self.modrc_dir.joinpath('packages')

    def tearDown(self):
        self.temp.cleanup()

    def test_create_package_dir(self):
        """Test the creation of a new package directory."""
        new_package_name = 'test-package'
        new_package_dir = package.create_package(self.modrc_dir, new_package_name)
        self.assertEqual(new_package_dir, self.packages_dir.joinpath(new_package_name))
        self.assertTrue(new_package_dir.exists())

    def test_create_package_yml(self):
        """Test the creation of the package.yml file"""
        new_package_name = 'test-package'
        new_package_dir = package.create_package(self.modrc_dir, new_package_name)
        new_package_yml = new_package_dir.joinpath('package.yml')
        self.assertTrue(new_package_yml.is_file())
