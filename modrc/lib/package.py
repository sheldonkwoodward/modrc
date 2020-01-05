import re
import yaml

import git

from modrc import exceptions
from modrc.lib import helper


def create_package(package_name, repo_url=None, default=False):
    """Create a new ModRC package.

    Parameters
    ----------
    package_name : str
        The name of the new package.
    repo_url : str
        The URL of the packages repository.
    default : boolean
        Whether the package should be set as the new default.

    Returns
    -------
    :obj:`Path`
        The path to the new package.

    Raises
    ------
    ModRCIntegrityError
        Raised if either the ModRC or packages directory do not exist.
    ModRCPackageExistsError
        Raised if the package already exists.
    """
    # TODO: validate repo url #52
    # get the packges directory
    packages_dir = helper.get_packages_dir()
    # define the package directories and files
    new_package_dir = packages_dir.joinpath(package_name)
    new_package_yml = new_package_dir.joinpath('package.yml')
    # raise a ModRCPackageExistsError if the package is already installed
    if new_package_dir.exists():
        raise exceptions.ModRCPackageExistsError("Package is already installed")
    # create the package directories and files
    new_package_dir.mkdir()
    new_package_yml.touch()
    # initialize the package as a git repo
    repo = git.Repo.init(str(new_package_dir))
    # add the repo url to package.yml if it was passed into the method
    if repo_url is not None:
        package_file = new_package_dir.joinpath('package.yml')
        with open(str(package_file), 'r') as yf:
            package_yaml = yaml.safe_load(yf)
            if package_yaml is None:
                package_yaml = {}
        package_yaml['repourl'] = repo_url
        # write to the package.yml
        with open(str(package_file), 'w') as yf:
            yaml.safe_dump(package_yaml, yf, default_flow_style=False)
        # add the repo url as the repo origin
        repo.create_remote('origin', url=repo_url)
    # commit package.yml to the package git repo and
    repo.index.add(['package.yml'])
    repo.index.commit('{} package initialization.'.format(package_name))
    # set the package as default in modrc.yml
    if default:
        set_default(package_name)
    return new_package_dir

def install_package(repo_url, default=False):
    """Install a new ModRC package.

    Parameters
    ----------
    repo_url : str
        The URL of the packages repository.
    default : boolean
        Whether the package should be set as the new default.

    Raises
    ------
    ModRCIntegrityError
        Raised if either the ModRC or packages directory do not exist.
    ModRCPackageExistsError
        Raised if the package already exists.
    ModRCGitError
        Raised if the package name could not be inferred from the repo URL.
    """
    # TODO: validate repo url #52
    # parse package name from repo url
    name_search = re.search(r'([^\/]+)\.git', repo_url)
    if name_search is not None:
        package_name = name_search.group(1)
    else:
        raise exceptions.ModRCGitError("Package name could not be inferred from repo URL.")
    # get the packges directory
    packages_dir = helper.get_packages_dir()
    # define the package directories and files
    package_dir = packages_dir.joinpath(package_name)
    # raise a ModRCPackageExistsError if the package is already installed
    if package_dir.exists():
        raise exceptions.ModRCPackageExistsError("Package is already installed")
    # clone the repo
    package_dir.mkdir()
    git.Repo.clone_from(repo_url, str(package_dir))
    # check if the repo is a valid package
    if not package_dir.joinpath('package.yml').is_file():
        package_dir.rmdir()
        raise exceptions.ModRCPackageDoesNotExistError("Cloned repo is not a valid package")
    # set the package as the default package
    if default:
        set_default(package_name)
    return package_dir

def get_package(package_name):
    """Get a package by name.

    Parameters
    ----------
    package_name : str
        The name of the package to get.

    Returns
    -------
    :obj:`Path`
        The path to the package

    Raises
    ------
    ModRCIntegrityError
        Raised if the packages directory does not exist.
    ModRCPackageDoesNotExistError
        Raised if the package does not exist.
    """
    packages_dir = helper.get_packages_dir()
    new_package_dir = packages_dir.joinpath(package_name)
    if not new_package_dir.is_dir():
        raise exceptions.ModRCPackageDoesNotExistError('Package does not exist')
    return new_package_dir

def get_package_file(package_name):
    """Get a package.yml file by package name.

    Parameters
    ----------
    package_name : str
        The name of the package to get the package.yml file from.

    Returns
    -------
    :obj:`Path`
        The path to the package.yml file.

    Raises
    ------
    ModRCIntegrityError
        Raised if the packages directory does not exist.
    ModRCPackageDoesNotExistError
        Raised if the package or package.yml file does not exist.
    """
    package_dir = get_package(package_name)
    package_file = package_dir.joinpath('package.yml')
    if not package_file.is_file():
        raise exceptions.ModRCPackageDoesNotExistError
    return package_file

def set_default(package_name):
    """Set a package as the default package.

    Parameters
    ----------
    package_name : str
        The name of the package to set as default.

    Raises
    ------
    ModRCIntegrityError
        Raised if the packages directory does not exist.
    ModRCPackageDoesNotExistError
        Raised if the package or package.yml file does not exist.
    """
    # verify the package exists
    get_package_file(package_name)
    # set the package as default
    modrc_file = helper.get_modrc_file()
    with open(str(modrc_file), 'r') as mf:
        modrc_yaml = yaml.safe_load(mf)
        if modrc_yaml is None:
            modrc_yaml = {}
    modrc_yaml['defaultpackage'] = package_name
    with open(str(modrc_file), 'w') as mf:
        yaml.safe_dump(modrc_yaml, mf, default_flow_style=False)
