# sheldon woodward
# 4/15/18

"""The setup command."""


import click
from clint import textui

from modrc import exceptions
from modrc.lib import setup as modrc_setup


@click.group()
def setup():
    """Install or uninstall ModRC."""
    pass

@setup.command()
def install():
    """Install ModRC into the current user's home folder."""
    # context
    debug = click.get_current_context().obj['debug']
    # try to install ModRC
    success = True
    try:
        modrc_setup.initial_setup()
    except exceptions.ModRCIntegrityError:
        # re-raise the exception if debugging is on
        if debug:
            raise
        success = False
    # react to the outcome of the command
    if success:
        textui.puts('ModRC installed at ~/.modrc')
    else:
        textui.puts(textui.colored.red('ModRC is already installed'))

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
        textui.puts('ModRC uninstalled at ~/.modrc')
    else:
        textui.puts('ModRC is not currently installed')
