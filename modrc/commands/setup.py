import click

from modrc import exceptions
from modrc.lib import setup as modrc_setup
from modrc.lib import package as modrc_package


@click.group()
def setup():
    """Install or uninstall ModRC."""
    pass

@setup.command()
def install():
    """Install ModRC into the current user's home folder."""
    # SETUP
    # get the debug context
    debug = click.get_current_context().obj['debug']

    # INTERACTIVE
    # choose package creation or installation
    package_name, repo_url = prompt_package_creation_installation()
    # choose the default editor
    editor = click.prompt('File editor', default='vim')
    # choose to automatically compile default package changes
    auto_compile = click.confirm('Automatically compile changes?', default=True)
    # choose to automatically sync default package changes
    auto_sync = click.confirm('Automatically sync changes?', default=True)

    # INSTALLATION
    # try to install ModRC
    success = True
    try:
        # setup the ModRC dir
        modrc_setup.initial_setup()
        # set the system configuration settings
        modrc_setup.populate_modrc_file(default_package=package_name, editor=editor, auto_compile=auto_compile, auto_sync=auto_sync)
        # create a new package
        if package_name is not None:
            modrc_package.create_package(package_name, repo_url=repo_url)
        # clone an existing package
        elif repo_url is not None:
            # TODO: clone the package from the URL
            pass
    except exceptions.ModRCIntegrityError:
        # re-raise the exception if debugging is on
        if debug:
            raise
        success = False
    # set the default editor

    # FINISH
    # react to the outcome of the installation
    if success:
        click.echo('ModRC successfully installed at ~/.modrc')
    else:
        click.secho('ModRC is already installed', fg='red', bold=True)

@setup.command()
def uninstall():
    """Uninstall ModRC from the current user's home folder."""
    # context
    debug = click.get_current_context().obj['debug']
    # try to uninstall ModRC
    success = True
    try:
        modrc_setup.teardown()
    except exceptions.ModRCIntegrityError:
        if debug:
            raise
        success = False
    # react to the outcome of the command
    if success:
        click.echo('ModRC uninstalled at ~/.modrc')
    else:
        click.echo('ModRC is not currently installed')

def prompt_package_creation_installation():
    package_name = None
    repo_url = None
    # create new package
    if click.confirm('Create a new package'):
        package_name = click.prompt('Package name')
        # add repo to package
        if click.confirm('Add repo clone URL'):
            repo_url = click.prompt('Repo clone URL')
    # install existing package
    elif click.confirm('Add an existing package repo', default=True):
        repo_url = click.prompt('Repo clone URL')
    return package_name, repo_url
