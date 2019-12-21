import pathlib
import tempfile
import unittest
import yaml

from modrc import exceptions
from modrc.lib import helper, package, setup


class TestCreatePackage(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = pathlib.Path(self.temp.name)
        setup.initial_setup(self.temp_dir)
        setup.populate_modrc_file(editor='vim', auto_compile=True, auto_sync=True)
        self.packages_dir = helper.get_packages_dir()

    def tearDown(self):
        # destroy the ModRC symlink
        setup.teardown(ignore_errors=True)
        # destroy the temp directory
        self.temp.cleanup()

    def test_package_already_exists(self):
        """Test that an exception is raised if the package already exists."""
        new_package_name = 'test-package'
        package.create_package(new_package_name)
        with self.assertRaises(exceptions.ModRCPackageExistsError):
            package.create_package(new_package_name)

    def test_create_package_dir(self):
        """Test the creation of a new package directory."""
        new_package_name = 'test-package'
        new_package_dir = package.create_package(new_package_name)
        self.assertEqual(new_package_dir, self.packages_dir.joinpath(new_package_name))
        self.assertTrue(new_package_dir.exists())

    def test_create_package_yml(self):
        """Test the creation of the package.yml file."""
        new_package_dir = package.create_package('test-package')
        new_package_yml = new_package_dir.joinpath('package.yml')
        self.assertTrue(new_package_yml.is_file())

    def test_add_repo_url(self):
        """Test that the repo URL is added to the package.yml file."""
        package.create_package('test-package', repo_url='https://url.example')
        package_file = package.get_package_file('test-package')
        with open(str(package_file), 'r') as yf:
            package_yaml = yaml.safe_load(yf)
        self.assertIn('repourl', package_yaml)
        self.assertEqual(package_yaml['repourl'], 'https://url.example')

    def test_set_default(self):
        """Test that the package is set as the default in the modrc.yml file."""
        package.create_package('test-package', default=True)
        modrc_file = helper.get_modrc_file()
        with open(str(modrc_file), 'r') as mf:
            modrc_yaml = yaml.safe_load(mf)
        self.assertIn('defaultpackage', modrc_yaml)
        self.assertEqual(modrc_yaml['defaultpackage'], 'test-package')


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


class TestGetPackageFile(unittest.TestCase):
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

    def test_package_dir_does_not_exist(self):
        """Test functionality when a package does not exist."""
        with self.assertRaises(exceptions.ModRCPackageDoesNotExistError):
            package.get_package_file('test-package')

    def test_package_file_does_not_exist(self):
        """Test functionality when a package file does not exist."""
        packages_dir = helper.get_packages_dir()
        packages_dir.joinpath('test-package').mkdir()
        with self.assertRaises(exceptions.ModRCPackageDoesNotExistError):
            package.get_package_file('test-package')

    def test_package_exists(self):
        """Test that the package.yml file is retrieved successfully."""
        package_dir = package.create_package('test-package')
        package_file = package.get_package_file('test-package')
        self.assertEqual(package_dir.joinpath('package.yml'), package_file)
        self.assertTrue(package_file.is_file())
