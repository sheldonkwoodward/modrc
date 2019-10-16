# sheldon woodward
# 4/15/18

"""The ping command."""


import click
from clint.textui import puts, colored


@click.command()
def ping():
    puts(colored.red('pong'))
