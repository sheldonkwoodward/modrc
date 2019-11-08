from modrc.lib import helper

def create_package(package_name):
    """Create a new ModRC package.

    Parameters
    ----------
    package_name : str
        The name of the new package.

    Returns
    -------
    :obj:`Path`
        The path to the new package.

    Raises
    ------
    FileNotFoundError
        Raised if either the ModRC or packages directory do not exist.
    """
    # get the packges directory
    packages_dir = helper.get_packages_dir()
    # define the package directories and files
    new_package_dir = packages_dir.joinpath(package_name)
    new_package_yml = new_package_dir.joinpath('package.yml')
    # create the package directories and files
    new_package_dir.mkdir()
    new_package_yml.touch()
    return new_package_dir

def get_package(package_name):
    """Get a package by name.

    Parameters
    ----------
    package_name : str
        The name of the package to get.

    Returns
    -------
    :obj:`Path`
        The path the package

    Raises
    ------
    FileNotFoundError
        Raised if the package does not exist.
    """
    packages_dir = helper.get_packages_dir()
    new_package_dir = packages_dir.joinpath(package_name)
    if not new_package_dir.is_dir():
        raise FileNotFoundError('Package does not exist')
    return new_package_dir

def create_file(file_name, package_name):
    """Create a new file in a package.

    Parameters
    ----------
    file_name : str
        The name of the file to create.
    package_name : str
        The name of the package that the file will go in.

    Returns
    -------
    :obj:`Path`
        Returns the path to the new file.

    Raises
    ------
    FileNotFoundError
        Raised if the package could not be found.
    FileExistsError
        Raised if the file already exists in the package.
    """
    # try to get the package
    try:
        package_dir = get_package(package_name)
    except FileNotFoundError:
        raise FileNotFoundError('Package does not exist')
    # check if the file already exists
    file_dir = package_dir.joinpath('files', file_name)
    if file_dir.is_dir():
        raise FileExistsError('File already exists')
    # create the file dir
    file_dir.mkdir(parents=True)
    return file_dir

