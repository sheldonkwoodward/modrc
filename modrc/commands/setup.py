# sheldon woodward
# 4/15/18

"""The setup command."""


import click
from clint import textui

from modrc import exceptions
from modrc.lib import setup as modrc_setup


@click.command()
def setup():
    # context
    debug = click.get_current_context().obj['debug']
    # try to setup ModRC
    success = True
    try:
        modrc_setup.initial_setup()
    except exceptions.ModRCIntegrityError:
        # re-raise the exception if debugging is on
        if debug:
            raise
        success = False

    # react to outcome of command
    if success:
        textui.puts('Setup complete')
    else:
        textui.puts(textui.colored.red('Setup failed! A ModRC directory already exists here.'))
