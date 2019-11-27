# pylint: disable=no-self-use

from unittest import mock

import pytest

from modrc import __main__
from modrc.lib import setup

class TestSetupNonInteractive:
    @pytest.mark.usefixtures('teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_modrc_already_installed(self, click_runner):
        """Test that initial setup is not called if ModRC is already installed."""
        setup.initial_setup()
        with mock.patch('modrc.lib.setup.initial_setup') as initial_setup:
            result = click_runner.invoke(__main__.main, ['setup', 'install', '--ni'])
        assert not initial_setup.called
        assert result.exit_code == 2

    @pytest.mark.usefixtures('teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_initial_setup_called(self, click_runner):
        """Test that initial setup is called if ModRC is not installed."""
        with mock.patch('modrc.lib.setup.initial_setup') as initial_setup:
            result = click_runner.invoke(__main__.main, ['setup', 'install', '--ni'])
        initial_setup.assert_called_once_with()
        assert result.exit_code == 0

    @pytest.mark.usefixtures('teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_non_interactive_defaults(self, click_runner):
        """Test the default values used if no options are given in non-interactive setup."""
        pmf = 'modrc.lib.setup.populate_modrc_file'
        cp = 'modrc.lib.package.create_package'
        with mock.patch(pmf) as populate_modrc_file, mock.patch(cp) as create_package:
            result = click_runner.invoke(__main__.main, ['setup', 'install', '--ni'])
        populate_modrc_file.assert_called_once_with(None, 'vim', False, False)
        assert not create_package.called
        # TODO: setup command URL clone option #44
        assert result.exit_code == 0

    # TODO: setup command URL clone option #44

    @pytest.mark.usefixtures('teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_url_and_name_option(self, click_runner):
        """Test that a package is created with the proper name and has the proper repo URL."""
        with mock.patch('modrc.lib.package.create_package') as create_package:
            result = click_runner.invoke(__main__.main, ['setup', 'install', '--ni', '--name', 'test-package', '--url', 'http://example.com'])
        create_package.assert_called_once_with('test-package', repo_url='http://example.com')
        # TODO: setup command URL clone option #44
        assert result.exit_code == 0

    @pytest.mark.usefixtures('teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_name_option(self, click_runner):
        """Test that a package is created with the proper name."""
        with mock.patch('modrc.lib.package.create_package') as create_package:
            result = click_runner.invoke(__main__.main, ['setup', 'install', '--ni', '--name', 'test-package'])
        create_package.assert_called_once_with('test-package', repo_url=None)
        # TODO: setup command URL clone option #44
        assert result.exit_code == 0

    @pytest.mark.usefixtures('teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_editor_option(self, click_runner):
        """Test that the specified editor is set."""
        with mock.patch('modrc.lib.setup.populate_modrc_file') as populate_modrc_file:
            result = click_runner.invoke(__main__.main, ['setup', 'install', '--ni', '--editor', 'nano'])
        populate_modrc_file.assert_called_once_with(None, 'nano', False, False)
        assert result.exit_code == 0

    @pytest.mark.usefixtures('teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_auto_compile_flag(self, click_runner):
        """Test that auto compile is turned on."""
        with mock.patch('modrc.lib.setup.populate_modrc_file') as populate_modrc_file:
            result = click_runner.invoke(__main__.main, ['setup', 'install', '--ni', '--auto-compile'])
        populate_modrc_file.assert_called_once_with(None, 'vim', True, False)
        assert result.exit_code == 0

    @pytest.mark.usefixtures('teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_auto_sync_flag(self, click_runner):
        """Test that auto sync is turned on."""
        with mock.patch('modrc.lib.setup.populate_modrc_file') as populate_modrc_file:
            result = click_runner.invoke(__main__.main, ['setup', 'install', '--ni', '--auto-sync'])
        populate_modrc_file.assert_called_once_with(None, 'vim', False, True)
        assert result.exit_code == 0

# TODO: setup command interactive testing #43
