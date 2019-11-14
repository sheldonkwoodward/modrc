import pathlib
import tempfile
import unittest

from modrc import exceptions
from modrc.lib import helper, package, setup


class TestCreatePackage(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = pathlib.Path(self.temp.name)
        setup.initial_setup(self.temp_dir)
        self.packages_dir = helper.get_packages_dir()

    def tearDown(self):
        # destroy the ModRC symlink
        setup.teardown(ignore_errors=True)
        # destroy the temp directory
        self.temp.cleanup()

    def test_create_package_dir(self):
        """Test the creation of a new package directory."""
        new_package_name = 'test-package'
        new_package_dir = package.create_package(new_package_name)
        self.assertEqual(new_package_dir, self.packages_dir.joinpath(new_package_name))
        self.assertTrue(new_package_dir.exists())

    def test_create_package_yml(self):
        """Test the creation of the package.yml file"""
        new_package_name = 'test-package'
        new_package_dir = package.create_package(new_package_name)
        new_package_yml = new_package_dir.joinpath('package.yml')
        self.assertTrue(new_package_yml.is_file())


class TestGetPackage(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = pathlib.Path(self.temp.name)
        setup.initial_setup(self.temp_dir)

    def tearDown(self):
        # destroy the ModRC symlink
        setup.teardown(ignore_errors=True)
        # destroy the temp directory
        self.temp.cleanup()

    def test_package_does_not_exist(self):
        """Test functionality when a package does not exist."""
        with self.assertRaises(exceptions.ModRCPackageDoesNotExistError):
            package.get_package('test-package')

    def test_package_exists(self):
        """Test retrieval of a package."""
        test_package = package.create_package('test-package')
        self.assertEqual(test_package, package.get_package('test-package'))
