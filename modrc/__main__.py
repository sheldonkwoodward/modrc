import click

import modrc
from modrc.commands import package
from modrc.commands import setup


@click.group()
@click.version_option(version=modrc.__version__)
def main():
    """The CLI to make managing your files across systems easier."""

# commands
main.add_command(setup)
main.add_command(package)
