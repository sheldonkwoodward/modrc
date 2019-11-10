from modrc import exceptions
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

def get_file(file_name, package_name):
    """Retrieve a file from a package.

    Parameters
    ----------
    file_name : str
        The name of the file to retrieve.
    package_name : str
        The name of the package that the file is in.

    Returns
    -------
    :obj:`Path`
        Returns the path to the file.

    Raises
    ------
    FileNotFoundError
        Raised if the file of package is not found.
    """
    # try to get the package directory
    try:
        package_dir = package.get_package(package_name)
    except FileNotFoundError:
        raise FileNotFoundError('Package does not exist')
    # try to the file directory
    file_dir = package_dir.joinpath('files', file_name)
    if not file_dir.is_dir():
        raise FileNotFoundError('File does not exist')
    return file_dir

def create_file_filter(filter_name, file_name, package_name):
    """Create a new file filter for a file.

    Parameters
    ----------
    filter_name : str
        The name of the new filter.
    file_name : str
        The file to create the filter for.
    package_name : str
        The package that the file is in.

    Returns
    -------
    :obj:`Path`
        Returns the path to the new file filter.

    Raises
    ------
    FileNotFoundError
        Raised if the package or file is not found.
    FilterNameError
        Raised if the filter name is invalid.
    """
    # try to get the file
    try:
        file_dir = get_file(file_name, package_name)
    except FileNotFoundError:
        raise FileNotFoundError('Package or file does not exist')
    # validate file filter name
    if not helper.valid_filter_name(filter_name):
        raise exceptions.FilterNameError('Invalid file filter name')
    # create the file filter
    file_filter = file_dir.joinpath(filter_name)
    file_filter.touch()
    return file_filter

def compile_file(file_name, system, package_name):
    """Compile a given file from a package.

    Parameters
    ----------
    file_name : str
        The name of the file to compile.
    system : str
        The version string for the system, same format as filter names.
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
    # try to get the file
    try:
        file_dir = get_file(file_name, package_name)
    except FileNotFoundError:
        raise FileNotFoundError('Package or file does not exist')
    # create the compiled file
    compiled_file = helper.get_live_dir().joinpath(file_name)
    compiled_file.touch()
    # iterate over all file filters and write their contents to the compiled file
    for file_filter in file_dir.iterdir():
        # skip files that do not match part of the system string
        if str(file_filter.name) != 'global' and system.find(str(file_filter.name)) != 0:
            continue
        # concatenate the filter to the end of the compiled file
        with open(str(compiled_file), 'a') as cf, open(str(file_filter), 'r') as ff:
            for line in ff.readlines():
                cf.write(line)
    # return the path to the compiled file
    return compiled_file

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
