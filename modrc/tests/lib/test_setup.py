import pathlib
import tempfile
import unittest

from modrc.lib import setup


class TestSetup(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.parentdir = pathlib.Path(self.temp.name)

    def tearDown(self):
        # destroy the temp directory
        self.temp.cleanup()

    def test_create_modrc_directory(self):
        """Test ModRC directory creation."""
        modrc_dir = setup.create_modrc_directory(self.parentdir)
        self.assertEqual(modrc_dir.name, '.modrc')
        self.assertTrue(modrc_dir.exists())

    def test_create_modrc_custom_directory(self):
        """Test custom modrc directory name."""
        modrc_dir = setup.create_modrc_directory(self.parentdir, '.custom')
        self.assertEqual(modrc_dir.name, '.custom')
        self.assertTrue(modrc_dir.exists())


# runner
if __name__ == '__main__':
    unittest.main()
