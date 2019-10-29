def verify_modrc_dir(modrc_dir):
    """Verify that the ModRC directory exist and is valid at a given location.

    Parameters
    ----------
    modrc_dir : :obj:`Path`
        The directory to verify as the ModRC directory.

    Returns
    -------
    bool
        Always returns True unless an exception is thrown.

    Raises
    ------
    FileNotFoundError
        Raised if the .modrc file does not exist at the given location.
    """
    # raise an exception the ModRC is not valid
    modrc_file = modrc_dir.joinpath('.modrc')
    if not modrc_file.is_file():
        raise FileNotFoundError('Not a valid ModRC directory')
    # return True if the ModRC directory is valid
    return True

def get_packages_dir(modrc_dir):
    """Get the packages directory within the ModRC directory.

    Parameters
    ----------
    modrc_dir : :obj:`Path`
        The ModRC directory.

    Returns
    -------
    :obj:`Path`
        The path to the packages directory.

    Raises
    ------
    FileNotFoundException
        Raised if the ModRC directory is invalid or the packages directory does not exist in it.
    """
    verify_modrc_dir(modrc_dir)
    packages_dir = modrc_dir.joinpath('packages')
    if not packages_dir.is_dir():
        raise FileNotFoundError('Packages directory does not exist')
    return packages_dir

def get_live_dir(modrc_dir):
    """Get the live directory within the ModRC directory.

    Parameters
    ----------
    modrc_dir : :obj:`Path`
        The ModRC directory.

    Returns
    -------
    :obj:`Path`
        The path to the live directory.

    Raises
    ------
    FileNotFoundException
        Raised if the ModRC directory is invalid or the live directory does not exist in it.
    """
    verify_modrc_dir(modrc_dir)
    live_dir = modrc_dir.joinpath('live')
    if not live_dir.is_dir():
        raise FileNotFoundError('Live directory does not exist')
    return live_dir
