def create_modrc_directory(parent_dir, modrc_dirname='.modrc'):
    # resolve the user directory
    parent_dir = parent_dir.expanduser()
    # create the modrc directory path
    modrc_dir = parent_dir.joinpath(modrc_dirname)
    # create the modrc dir
    modrc_dir.mkdir()
    return modrc_dir
