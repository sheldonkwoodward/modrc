# pylint: disable=no-self-use

from unittest import mock

import pytest

from modrc import __main__, exceptions
from modrc.lib import helper


class TestAddNonInteractive:
    @pytest.mark.usefixtures('click_runner')
    def test_modrc_not_installed(self, click_runner):
        """Test that a warning is shown if ModRC is not installed."""
        with mock.patch('modrc.lib.package.create_package', side_effect=exceptions.ModRCIntegrityError()) as create_package:
            result = click_runner.invoke(__main__.main, ['package', 'add', 'test-package'])
        create_package.assert_called_once_with('test-package', repo_url=None, default=False)
        assert result.exit_code == 2

    @pytest.mark.usefixtures('setup_teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_package_already_exists(self, click_runner):
        """Test that an existing package with the same name is detected."""
        with mock.patch('modrc.lib.package.create_package', side_effect=exceptions.ModRCPackageExistsError()) as create_package:
            result = click_runner.invoke(__main__.main, ['package', 'add', 'test-package'])
        create_package.assert_called_once_with('test-package', repo_url=None, default=False)
        assert result.exit_code == 2

    @pytest.mark.usefixtures('setup_teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_package_create(self, click_runner):
        """Test that package_create is called and was successful."""
        with mock.patch('modrc.lib.package.create_package', return_value=helper.get_packages_dir().joinpath('test-package')) as create_package:
            result = click_runner.invoke(__main__.main, ['package', 'add', 'test-package'])
        create_package.assert_called_once_with('test-package', repo_url=None, default=False)
        assert result.exit_code == 0

    @pytest.mark.usefixtures('setup_teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_package_default(self, click_runner):
        """Test that the new package is set as default if the flag is passed."""
        with mock.patch('modrc.lib.package.create_package', return_value=helper.get_packages_dir().joinpath('test-package')) as create_package:
            result = click_runner.invoke(__main__.main, ['package', 'add', '--default', 'test-package'])
        create_package.assert_called_once_with('test-package', repo_url=None, default=True)
        assert result.exit_code == 0

    @pytest.mark.usefixtures('setup_teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_package_non_default(self, click_runner):
        """Test that the new package is not set as default by default."""
        with mock.patch('modrc.lib.package.create_package', return_value=helper.get_packages_dir().joinpath('test-package')) as create_package:
            result = click_runner.invoke(__main__.main, ['package', 'add', 'test-package'])
        create_package.assert_called_once_with('test-package', repo_url=None, default=False)
        assert result.exit_code == 0

    @pytest.mark.usefixtures('setup_teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_package_create_url(self, click_runner):
        """Test that the new package is created with the URL option."""
        with mock.patch('modrc.lib.package.create_package', return_value=helper.get_packages_dir().joinpath('test-package')) as create_package:
            result = click_runner.invoke(__main__.main, ['package', 'add', '--url', 'git@github.com:test/test.git', 'test-package'])
        create_package.assert_called_once_with('test-package', repo_url='git@github.com:test/test.git', default=False)
        assert result.exit_code == 0


class TestInstallNonInteractive:
    @pytest.mark.usefixtures('setup_teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_modrc_not_installed(self, click_runner):
        """Test that a warning is shown if ModRC is not installed."""
        with mock.patch('modrc.lib.package.install_package', side_effect=exceptions.ModRCIntegrityError()) as install_package:
            result = click_runner.invoke(__main__.main, ['package', 'install', 'git@github.com:test/test-package.git'])
        install_package.assert_called_once_with('git@github.com:test/test-package.git', default=False)
        assert result.exit_code == 2

    @pytest.mark.usefixtures('setup_teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_package_already_exists(self, click_runner):
        """Test that an existing package with the same name is detected."""
        with mock.patch('modrc.lib.package.install_package', side_effect=exceptions.ModRCPackageExistsError()) as install_package:
            result = click_runner.invoke(__main__.main, ['package', 'install', 'git@github.com:test/test-package.git'])
        install_package.assert_called_once_with('git@github.com:test/test-package.git', default=False)
        assert result.exit_code == 2

    @pytest.mark.usefixtures('setup_teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_package_name_unknown(self, click_runner):
        """Test that a URL with an unknwn package name is detected."""
        with mock.patch('modrc.lib.package.install_package', side_effect=exceptions.ModRCGitError()) as install_package:
            result = click_runner.invoke(__main__.main, ['package', 'install', 'git@github.com:test.git'])
        install_package.assert_called_once_with('git@github.com:test.git', default=False)
        assert result.exit_code == 2

    @pytest.mark.usefixtures('setup_teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_package_install(self, click_runner):
        """Test that install_package is called and was successful."""
        with mock.patch('modrc.lib.package.install_package', return_value=helper.get_packages_dir().joinpath('test-package')) as install_package:
            result = click_runner.invoke(__main__.main, ['package', 'install', 'git@github.com:test/test-package.git'])
        install_package.assert_called_once_with('git@github.com:test/test-package.git', default=False)
        assert result.exit_code == 0

    @pytest.mark.usefixtures('setup_teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_package_default(self, click_runner):
        """Test that the package is set as default if the flag is passed."""
        with mock.patch('modrc.lib.package.install_package', return_value=helper.get_packages_dir().joinpath('test-package')) as install_package:
            result = click_runner.invoke(__main__.main, ['package', 'install', '--default', 'git@github.com:test/test-package.git'])
        install_package.assert_called_once_with('git@github.com:test/test-package.git', default=True)
        assert result.exit_code == 0

    @pytest.mark.usefixtures('setup_teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_package_non_default(self, click_runner):
        """Test that the package is not set as default if the flag is passed."""
        with mock.patch('modrc.lib.package.install_package', return_value=helper.get_packages_dir().joinpath('test-package')) as install_package:
            result = click_runner.invoke(__main__.main, ['package', 'install', 'git@github.com:test/test-package.git'])
        install_package.assert_called_once_with('git@github.com:test/test-package.git', default=False)
        assert result.exit_code == 0


class TestDefault:
    @pytest.mark.usefixtures('setup_teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_modrc_not_installed(self, click_runner):
        """Test that a warning is shown if ModRC is not installed."""
        with mock.patch('modrc.lib.package.set_default', side_effect=exceptions.ModRCIntegrityError()) as set_default:
            result = click_runner.invoke(__main__.main, ['package', 'default', 'test-package'])
        set_default.assert_called_once_with('test-package')
        assert result.exit_code == 2

    @pytest.mark.usefixtures('setup_teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_package_does_not_exist(self, click_runner):
        """Test that a warning is shown if the package does not exist."""
        with mock.patch('modrc.lib.package.set_default', side_effect=exceptions.ModRCPackageDoesNotExistError()) as set_default:
            result = click_runner.invoke(__main__.main, ['package', 'default', 'test-package'])
        set_default.assert_called_once_with('test-package')
        assert result.exit_code == 2

    @pytest.mark.usefixtures('setup_teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_set_default(self, click_runner):
        """Test that the package is set as the default package."""
        with mock.patch('modrc.lib.package.set_default') as set_default:
            result = click_runner.invoke(__main__.main, ['package', 'default', 'test-package'])
        set_default.assert_called_once_with('test-package')
        assert result.exit_code == 0


class TestList:
    @pytest.mark.usefixtures('setup_teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_modrc_not_installed(self, click_runner):
        """Test that a warning is shown if ModRC is not installed."""
        with mock.patch('modrc.lib.package.list_packages', side_effect=exceptions.ModRCIntegrityError()) as list_packages:
            result = click_runner.invoke(__main__.main, ['package', 'list'])
        list_packages.assert_called_once_with()
        assert result.exit_code == 2

    @pytest.mark.usefixtures('setup_teardown')
    @pytest.mark.usefixtures('click_runner')
    def test_list_packages(self, click_runner):
        """Test that packages are listed."""
        with mock.patch('modrc.lib.package.list_packages', return_value=['test1', 'test2']) as list_packages:
            result = click_runner.invoke(__main__.main, ['package', 'list'])
        list_packages.assert_called_once_with()
        assert 'test1' in result.output
        assert 'test2' in result.output
        assert result.exit_code == 0
