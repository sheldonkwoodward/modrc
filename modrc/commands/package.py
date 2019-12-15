import click


@click.group()
def package():
    """Manage package installations."""

@package.command()
def add():
    click.echo("stub")
