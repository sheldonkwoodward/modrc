def create_modrc_directory(parent_dir, modrc_dirname='.modrc'):
    """Create the ModRC directory and its file structure.

    Parameters
    ----------
    parent_dir : :obj:`Path`
        The directory to create the ModRC directory in.
    modrc_dirname : str, optional
        A custom name for the ModRC directory.
    """
    # resolve the user directory
    parent_dir = parent_dir.expanduser()
    # create the modrc directory path
    modrc_dir = parent_dir.joinpath(modrc_dirname)
    packages_dir = modrc_dir.joinpath('packages')
    live_dir = modrc_dir.joinpath('live')
    # create the modrc directories
    modrc_dir.mkdir()
    packages_dir.mkdir()
    live_dir.mkdir()
    return modrc_dir
