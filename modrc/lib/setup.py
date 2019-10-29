import pathlib


def initial_setup(parent_dir='~', symlink=False):
    """The initial setup process for ModRC to create the ModRC directory and its file structure.

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
    modrc_dir = parent_dir.joinpath('.modrc')
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
    # symlink the ModRC directory if it is not in the user's home directory
    home_dir = pathlib.Path('~').expanduser()
    if symlink and parent_dir != home_dir:
        pathlib.Path('~/.modrc').symlink_to(modrc_dir)
    # return the path to the new modrc_dir
    return modrc_dir
