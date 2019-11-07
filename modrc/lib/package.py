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
