import pathlib
import shutil


def initial_setup(symlink=None):
    """The initial setup process for ModRC to create the ModRC directory and its file structure.

    Parameters
    ----------
    symlink : :obj:`Path` or None
        The path where actual ModRC files exist that should be symlinked to.

    Returns
    -------
    :obj:`Path`
        The path to the newly created ModRC directory

    Raises
    ------
    FileExistsError
        Raised if the ModRC direcotory with the specified name already exists.
    """
    # create the modrc directory
    modrc_dir = pathlib.Path('~/.modrc').expanduser()
    if modrc_dir.is_dir():
        raise FileExistsError('A ModRC directory is already here')
    elif symlink is None:
        modrc_dir.mkdir()
    else:
        modrc_dir.symlink_to(symlink.expanduser())
    # create files in the modrc directory
    modrc_file = modrc_dir.joinpath('.modrc')
    packages_dir = modrc_dir.joinpath('packages')
    live_dir = modrc_dir.joinpath('live')
    modrc_file.touch()
    packages_dir.mkdir()
    live_dir.mkdir()
    # symlink the ModRC directory if it is not in the user's home directory
    return modrc_dir


def teardown():
    """The teardown process for ModRC to delete the ModRC directory and its file structure.

    Returns
    -------
    bool
        Return True if anything was deleted, False if nothing was deleted.
    """
    # get the ModRC directory path
    modrc_dir = pathlib.Path('~/.modrc').expanduser()
    # delete a symlink
    if modrc_dir.is_symlink():
        modrc_dir.unlink()
        return True
    # delete a directory
    if modrc_dir.is_dir():
        shutil.rmtree(str(modrc_dir))
        return True
    # nothing was deleted
    return False
