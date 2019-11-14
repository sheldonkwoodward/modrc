# sheldon woodward
# 4/15/18

"""Main CLI entrypoint."""


import click

from .commands import setup


@click.group()
@click.option('--debug', is_flag=True, envvar='DEBUG')
@click.pass_context
def main(ctx, debug):
    """The CLI to make managing your files across systems easier."""
    # set global context
    ctx.obj = {
        'debug': debug
    }


# commands
main.add_command(setup)
