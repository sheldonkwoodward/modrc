import pathlib
import tempfile
import unittest
import yaml

import git

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

    def test_initialize_repo(self):
        """Test that the package is initialized as a new Git repo."""
        package_dir = package.create_package('test-package')
        self.assertEqual(git.Repo(str(package_dir)).git_dir, str(package_dir.joinpath('.git')))

    def test_commit_package_yaml(self):
        """Test that the package.yml file is committed to the new Git repo."""
        package_dir = package.create_package('test-package')
        repo = git.Repo(str(package_dir))
        tree = repo.head.commit.tree
        self.assertIn('package.yml', tree)

    def test_add_remote_origin(self):
        """Test that the the repo_url is set as origin if it was included."""
        package_dir = package.create_package('test-package', repo_url='git@github.com:test/test.git')
        repo = git.Repo(str(package_dir))
        self.assertIn('origin', repo.remotes)
        self.assertEqual(repo.remotes.origin.url, 'git@github.com:test/test.git')


class TestInstallPackage(unittest.TestCase):
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
        """Test that an excpetion is raised if the package already exists."""
        package.create_package('test-package')
        with self.assertRaises(exceptions.ModRCPackageExistsError):
            package.install_package('git@github.com:test/test-package.git')

    def test_clone_repo(self):
        """Test that the clones successfully."""
        with unittest.mock.patch('modrc.lib.package.git.Repo.clone_from') as clone:
            def side_effect(url, clone_dir):
                helper.get_packages_dir().joinpath('test-package/package.yml').touch()
            clone.side_effect = side_effect
            package_dir = package.install_package('git@github.com:test/test-package.git')
        clone.assert_called_once_with('git@github.com:test/test-package.git', str(helper.get_packages_dir().joinpath('test-package')))
        self.assertEqual(package_dir, self.packages_dir.joinpath('test-package'))
        self.assertTrue(package_dir.is_dir())

    def test_package_yaml_does_not_exist(self):
        """Test that the package is not installed if it does not have a packge.yml file."""
        with unittest.mock.patch('modrc.lib.package.git.Repo.clone_from'):
            with self.assertRaises(exceptions.ModRCPackageDoesNotExistError):
                package.install_package('git@github.com:test/test-package.git')
        self.assertFalse(helper.get_packages_dir().joinpath('test-package').exists())

    def test_set_default(self):
        """Test that the package is set as the default in the modrc.yml file."""
        with unittest.mock.patch('modrc.lib.package.git.Repo.clone_from') as clone:
            def side_effect(url, clone_dir):
                helper.get_packages_dir().joinpath('test-package/package.yml').touch()
            clone.side_effect = side_effect
            package.install_package('git@github.com:test/test-package.git', default=True)
        modrc_file = helper.get_modrc_file()
        with open(str(modrc_file), 'r') as mf:
            modrc_yaml = yaml.safe_load(mf)
        self.assertIn('defaultpackage', modrc_yaml)
        self.assertEqual(modrc_yaml['defaultpackage'], 'test-package')


class TestListPackages(unittest.TestCase):
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

    def test_no_packages_installed(self):
        """Test that an empty list is returned if no packages are installed."""
        self.assertEqual(package.list_packages(), [])

    def test_multiple_packages_installed(self):
        """Test that all installed package names are returned in a list."""
        package.create_package('test-package-1')
        package.create_package('test-package-2')
        packages = package.list_packages()
        self.assertIn('test-package-1', packages)
        self.assertIn('test-package-2', packages)


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


class TestSetDefault(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = pathlib.Path(self.temp.name)
        setup.initial_setup(self.temp_dir)
        setup.populate_modrc_file()

    def tearDown(self):
        # destroy the ModRC symlink
        setup.teardown(ignore_errors=True)
        # destroy the temp directory
        self.temp.cleanup()

    def test_package_does_not_exist(self):
        """Test functionality when the package does not exist."""
        with self.assertRaises(exceptions.ModRCPackageDoesNotExistError):
            package.set_default('test-package')

    def test_set_default(self):
        """Test that the package is set as the default in the modrc.yml file."""
        package.create_package('test-package', default=False)
        package.set_default('test-package')
        modrc_file = helper.get_modrc_file()
        with open(str(modrc_file), 'r') as mf:
            modrc_yaml = yaml.safe_load(mf)
        self.assertIn('defaultpackage', modrc_yaml)
        self.assertEqual(modrc_yaml['defaultpackage'], 'test-package')


class TestRemovePackage(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = pathlib.Path(self.temp.name)
        setup.initial_setup(self.temp_dir)
        setup.populate_modrc_file()

    def tearDown(self):
        # destroy the ModRC symlink
        setup.teardown(ignore_errors=True)
        # destroy the temp directory
        self.temp.cleanup()

    def test_package_does_not_exist(self):
        """Test functionality when the package does not exist."""
        with self.assertRaises(exceptions.ModRCPackageDoesNotExistError):
            package.remove_package('test-package')

    def test_remove_package(self):
        """Test that a package is successfully removed."""
        package.create_package('test-package')
        package_dir = package.get_package('test-package')
        package.remove_package('test-package')
        self.assertFalse(package_dir.exists())
