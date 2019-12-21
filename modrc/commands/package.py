import sys

import click

from modrc import exceptions
from modrc.lib import package as modrc_package


@click.group()
def package():
    """Manage package installations."""

@package.command()
@click.argument('name')
@click.option('-d', '--default', 'default', is_flag=True, help='Set the new package as the default package.')
@click.option('--url', 'repo_url', help='The URL to a package repo, should be an empty repo.')
def add(name, default, repo_url):
    try:
        modrc_package.create_package(name, repo_url=repo_url, default=default)
    except exceptions.ModRCIntegrityError:
        click.secho('ModRC is not installed', fg='red', bold=True)
        sys.exit(2)
    except exceptions.ModRCPackageExistsError:
        click.secho('Package {} already exists'.format(name), fg='red', bold=True)
        sys.exit(2)
    click.echo("Package {} has been created".format(name))
