import pathlib
import tempfile
import unittest

from modrc.lib import file, helper, package, setup


class TestCreateFile(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = pathlib.Path(self.temp.name)
        setup.initial_setup(self.temp_dir)

    def tearDown(self):
        # destroy the ModRC symlink
        setup.teardown()
        # destroy the temp directory
        self.temp.cleanup()

    def test_package_does_not_exist(self):
        """Test that an exception is raised when the package does not exist."""
        with self.assertRaises(FileNotFoundError):
            file.create_file('test-file', 'test-package')

    def test_file_already_exists(self):
        """Test that an exception is raised when the file already exists."""
        package_dir = package.create_package('test-package')
        package_dir.joinpath('files', 'test-file').mkdir(parents=True)
        with self.assertRaises(FileExistsError):
            file.create_file('test-file', 'test-package')

    def test_create_file_success(self):
        """Tests that the new file is created successfully."""
        package_dir = package.create_package('test-package')
        file_dir = file.create_file('test-file', 'test-package')
        self.assertEqual(package_dir.joinpath('files', 'test-file'), file_dir)
        self.assertTrue(file_dir.is_dir())


class TestCompileFile(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = pathlib.Path(self.temp.name)
        self.modrc_dir = setup.initial_setup(self.temp_dir)
        self.packages_dir = helper.get_packages_dir()
        package.create_package('test-package')

    def tearDown(self):
        # destroy the ModRC symlink
        setup.teardown()
        # destroy the temp directory
        self.temp.cleanup()

    def test_file_does_not_exist(self):
        """Tests that an error is thrown if the file does not exist."""
        with self.assertRaises(FileNotFoundError):
            file.compile_file('test-file', 'test-package')


class TestGetLiveFile(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = pathlib.Path(self.temp.name)
        setup.initial_setup(self.temp_dir)

    def tearDown(self):
        # destroy the ModRC symlink
        setup.teardown()
        # destroy the temp directory
        self.temp.cleanup()

    def test_live_file_does_not_exist(self):
        """Tests that an exception is thrown if a live file does not exist."""
        with self.assertRaises(FileNotFoundError):
            file.get_live_file('test-file')

    def test_live_file_exists(self):
        """Tests that a live file is retrieved if it exists."""
        live_file = helper.get_live_dir().joinpath('test-file')
        live_file.touch()
        self.assertEqual(file.get_live_file('test-file'), live_file)
