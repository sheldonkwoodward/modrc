import pathlib
import tempfile
import unittest

from modrc.lib import helper, setup


class TestVerifyModRCDir(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.parent_dir = pathlib.Path(self.temp.name)

    def tearDown(self):
        # destroy the temp directory
        self.temp.cleanup()

    def test_modrc_dir_does_not_exist(self):
        """Tests that a folder does not exist at the given path."""
        modrc_dir = self.parent_dir.joinpath('.modrc')
        with self.assertRaises(FileNotFoundError):
            helper.verify_modrc_dir(modrc_dir)

    def test_modrc_file_does_not_exist(self):
        """Tests that the .modrc file exists at the given path."""
        modrc_dir = self.parent_dir.joinpath('.modrc')
        modrc_dir.mkdir()
        with self.assertRaises(FileNotFoundError):
            helper.verify_modrc_dir(modrc_dir)

    def test_success(self):
        """Tests that the ModRC directory is valid at a given path."""
        modrc_dir = setup.initial_setup(self.parent_dir)
        self.assertTrue(helper.verify_modrc_dir(modrc_dir))


class TestGetPackagesDir(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.parent_dir = pathlib.Path(self.temp.name)

    def tearDown(self):
        # destroy the temp directory
        self.temp.cleanup()

    def test_invalid_modrc_dir(self):
        """Tests that a FileNotFoundError is raised for an invalid ModRC directory."""
        # create a path for a non-existant ModRC directory
        modrc_dir = self.parent_dir.joinpath('.modrc')
        modrc_dir.mkdir()
        # test that an exception is raised
        with self.assertRaises(FileNotFoundError):
            helper.get_packages_dir(modrc_dir)

    def test_packages_dir_does_not_exist(self):
        """Tests that a FileNotFoundError is raised if the packages directory does not exist."""
        # setup the ModRC directory without a packages directory
        modrc_dir = self.parent_dir.joinpath('.modrc')
        modrc_file = modrc_dir.joinpath('.modrc')
        modrc_dir.mkdir()
        modrc_file.touch()
        # test that an exception is raised
        with self.assertRaises(FileNotFoundError):
            helper.get_packages_dir(modrc_dir)

    def test_success(self):
        """Tests that the path for the packages directory is retrieved successfully."""
        modrc_dir = setup.initial_setup(self.parent_dir)
        packages_dir = modrc_dir.joinpath('packages')
        self.assertEqual(packages_dir, helper.get_packages_dir(modrc_dir))


class TestGetLiveDir(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.parent_dir = pathlib.Path(self.temp.name)

    def tearDown(self):
        # destroy the temp directory
        self.temp.cleanup()

    def test_invalid_modrc_dir(self):
        """Tests that a FileNotFoundError is raised for an invalid ModRC directory."""
        # create a path for a non-existant ModRC directory
        modrc_dir = self.parent_dir.joinpath('.modrc')
        modrc_dir.mkdir()
        # test that an exception is raised
        with self.assertRaises(FileNotFoundError):
            helper.get_live_dir(modrc_dir)

    def test_live_dir_does_not_exist(self):
        """Tests that a FileNotFoundError is raised if the live directory does not exist."""
        # setup the ModRC directory without a live directory
        modrc_dir = self.parent_dir.joinpath('.modrc')
        modrc_file = modrc_dir.joinpath('.modrc')
        modrc_dir.mkdir()
        modrc_file.touch()
        # test that an exception is raised
        with self.assertRaises(FileNotFoundError):
            helper.get_live_dir(modrc_dir)

    def test_success(self):
        """Tests that the path for the live directory is retrieved successfully."""
        modrc_dir = setup.initial_setup(self.parent_dir)
        live_dir = modrc_dir.joinpath('live')
        self.assertEqual(live_dir, helper.get_live_dir(modrc_dir))
