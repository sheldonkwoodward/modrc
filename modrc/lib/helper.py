import pathlib
import re


def verify_modrc_dir():
    """Verify that the ModRC directory exist and is valid.

    Returns
    -------
    bool
        Always returns True unless an exception is thrown.

    Raises
    ------
    FileNotFoundError
        Raised if the .modrc file does not exist at the given location.
    """
    # raise an exception if the ModRC directory is not valid
    modrc_dir = pathlib.Path('~/.modrc').expanduser()
    if not modrc_dir.is_dir():
        raise FileNotFoundError('Not a valid ModRC directory')
    # raise an exception if the ModRC file is not valid
    modrc_file = modrc_dir.joinpath('.modrc')
    if not modrc_file.is_file():
        raise FileNotFoundError('Not a valid ModRC directory')
    # return True if the ModRC directory is valid
    return True

def get_modrc_dir():
    """Try to find the ModRC directory automatically.

    Returns
    -------
    :obj:`Path`
        Return the path to the ModRC directory.

    Raises
    ------
    FileNotFoundError
        Raised if the ModRC directory could not be found automatically.
    """
    modrc_dir = pathlib.Path('~/.modrc').expanduser()
    if not verify_modrc_dir():
        raise FileNotFoundError('The ModRC directory could not be found')
    return modrc_dir

def get_packages_dir():
    """Get the packages directory within the ModRC directory.

    Returns
    -------
    :obj:`Path`
        The path to the packages directory.

    Raises
    ------
    FileNotFoundException
        Raised if the ModRC directory is invalid or the packages directory does not exist in it.
    """
    verify_modrc_dir()
    packages_dir = pathlib.Path('~/.modrc/packages').expanduser()
    if not packages_dir.is_dir():
        raise FileNotFoundError('Packages directory does not exist')
    return packages_dir

def get_live_dir():
    """Get the live directory within the ModRC directory.

    Returns
    -------
    :obj:`Path`
        The path to the live directory.

    Raises
    ------
    FileNotFoundException
        Raised if the ModRC directory is invalid or the live directory does not exist in it.
    """
    verify_modrc_dir()
    live_dir = pathlib.Path('~/.modrc/live').expanduser()
    if not live_dir.is_dir():
        raise FileNotFoundError('Live directory does not exist')
    return live_dir

def valid_filter_name(filter_name):
    """Validate a filter name.

    Parameters
    ----------
    filter_name
        The filter name to validate.

    Returns
    -------
    bool
        Return True if the name is valid, False if invalid.
    """
    # explicit matching
    if filter_name == 'global':
        return True
    # macos matching
    if re.fullmatch(r'macos(\.10(\.[0-9]+){0,2})?', filter_name):
        return True
    # linux matching
    if re.fullmatch(r'linux(\.[a-z]+(\.[0-9]+)*)?', filter_name):
        return True
    # MAC address matching
    if re.fullmatch(r'[0-9a-f]{12}', filter_name):
        return True
    return False
