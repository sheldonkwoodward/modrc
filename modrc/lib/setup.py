def create_modrc_directory(parent_dir, modrc_dirname='.modrc'):
    """Create the ModRC directory and its file structure.

    Parameters
    ----------
    parent_dir : :obj:`Path`
        The directory to create the ModRC directory in.
    modrc_dirname : str, optional
        A custom name for the ModRC directory.

    Returns
    -------
    :obj:`Path`
        The path to the newly created ModRC directory

    Raises
    ------
    FileExistsError
        Raised if the ModRC direcotory with the specified name already exists.
    """
    # resolve the user directory
    parent_dir = parent_dir.expanduser()
    # create the modrc directory path
    modrc_dir = parent_dir.joinpath(modrc_dirname)
    modrc_file = modrc_dir.joinpath('.modrc')
    packages_dir = modrc_dir.joinpath('packages')
    live_dir = modrc_dir.joinpath('live')
    # create the modrc directories
    try:
        modrc_dir.mkdir()
    except FileExistsError:
        raise FileExistsError('A ModRC directory is already here')
    modrc_file.touch()
    packages_dir.mkdir()
    live_dir.mkdir()
    return modrc_dir
