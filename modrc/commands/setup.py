import click

from modrc import exceptions
from modrc.lib import helper as modrc_helper
from modrc.lib import package as modrc_package
from modrc.lib import setup as modrc_setup


@click.group()
def setup():
    """Install or uninstall ModRC."""
    pass

@setup.command()
@click.option('--ni', '--non-interactive', 'non_interactive', is_flag=True, help='Toggle interactive setup off. Default settings will be used if not specified.')
@click.option('-u', '--url', 'repo_url', help='The URL to a package repository. Will be ignored if name is specified.')
@click.option('-n', '--name', 'package_name', help='The name of the new package.')
@click.option('-e', '--editor', default='vim', help='The default editor when opening files.')
@click.option('--ac', '--auto-compile', 'auto_compile', is_flag=True, help='Toggle auto-compile on.')
@click.option('--as', '--auto-sync', 'auto_sync', is_flag=True, help='Toggle auto-sync on.')
def install(non_interactive, repo_url, package_name, editor, auto_compile, auto_sync):
    """Install ModRC into the current user's home folder."""
    # SETUP
    # get the debug context
    debug = click.get_current_context().obj['debug']

    # check if ModRC is already installed
    try:
        if modrc_helper.verify_modrc_dir():
            click.secho('ModRC is already installed', fg='red', bold=True)
            exit(2)
    except exceptions.ModRCIntegrityError:
        pass

    try:
        # INTERACTIVE
        if not non_interactive:
            # choose package creation or installation
            package_name, repo_url = prompt_package_creation_installation()
            # choose the default editor
            editor = click.prompt('File editor', default='vim')
            # choose to automatically compile default package changes
            auto_compile = click.confirm('Automatically compile changes?', default=True)
            # choose to automatically sync default package changes
            auto_sync = click.confirm('Automatically sync changes?', default=True)

        # INSTALLATION
        # setup the ModRC dir
        modrc_setup.initial_setup()
        # set the system configuration settings
        modrc_setup.populate_modrc_file(package_name, editor, auto_compile, auto_sync)
        # create a new package
        if package_name is not None:
            modrc_package.create_package(package_name, repo_url=repo_url)
        # clone an existing package
        elif repo_url is not None:
            # TODO: setup command URL clone option #44
            pass
    except Exception:
        # re-raise the exception if debugging is on
        if debug:
            raise
        click.secho('An error occured. Run with --debug to see stack trace.', fg='red', bold=True)
    # set the default editor

    # FINISH
    # react to the outcome of the installation
    click.echo('ModRC successfully installed at ~/.modrc')

@setup.command()
def uninstall():
    """Uninstall ModRC from the current user's home folder."""
    # context
    debug = click.get_current_context().obj['debug']

    # uninstall ModRC
    try:
        # react to the outcome of the command
        if modrc_setup.teardown(ignore_errors=True):
            click.echo('ModRC uninstalled at ~/.modrc')
        else:
            click.echo('ModRC is not currently installed')
            exit(2)
    except exceptions.ModRCIntegrityError:
        # re-raise the exception if debugging is on
        if debug:
            raise
        click.secho('An error occured. Run with --debug to see stack trace.', fg='red', bold=True)

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
