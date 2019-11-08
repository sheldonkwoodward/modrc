from modrc.lib import helper, package


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
        package_dir = package.get_package(package_name)
    except FileNotFoundError:
        raise FileNotFoundError('Package does not exist')
    # check if the file already exists
    file_dir = package_dir.joinpath('files', file_name)
    if file_dir.is_dir():
        raise FileExistsError('File already exists')
    # create the file dir
    file_dir.mkdir(parents=True)
    return file_dir

def compile_file(file_name, package_name):
    """Compile a given file from a package.

    Parameters
    ----------
    file_name : str
        The name of the file to compile.
    package_name : str
        The name of the package that the file is in.

    Returns
    -------
    :obj:`Path`
        Returns the path to the live file.

    Raises
    ------
    FileNotFoundError
        Raised if the file or package could not be found.
    """
    raise FileNotFoundError('File does not exist')

def get_live_file(file_name):
    """Retrieve a live file.

    Parameters
    ----------
    file_name : str
        The name of the live file to retrieve.

    Returns
    -------
    :obj:`Path`
        Returns the path to the live file.

    Raises
    ------
    FileNotFoundError
        Raised if the live file does not exist.
    """
    # try and get the live file
    live_file = helper.get_live_dir().joinpath(file_name)
    if not live_file.is_file():
        raise FileNotFoundError('Live file does not exist')
    return live_file
