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
    """Create a new ModRC package."""
    try:
        modrc_package.create_package(name, repo_url=repo_url, default=default)
    except exceptions.ModRCIntegrityError:
        click.secho('ModRC is not installed', fg='red', bold=True)
        sys.exit(2)
    except exceptions.ModRCPackageExistsError:
        click.secho('Package {} already exists'.format(name), fg='red', bold=True)
        sys.exit(2)
    click.echo("Package {} has been created".format(name))

@package.command()
@click.argument('url')
@click.option('-d', '--default', 'default', is_flag=True, help='Set the package as the default package.')
def install(url, default):
    """Install an existing ModRC package with Git."""
    try:
        modrc_package.install_package(url, default=default)
    except exceptions.ModRCIntegrityError:
        click.secho('ModRC is not installed', fg='red', bold=True)
        sys.exit(2)
    except exceptions.ModRCPackageExistsError:
        click.secho('Package {} already exists'.format(url), fg='red', bold=True)
        sys.exit(2)
    except exceptions.ModRCGitError:
        click.secho('Package name could not be inferred, check your URL', fg='red', bold=True)
        sys.exit(2)
    click.echo("Package {} has been installed".format(url))

@package.command()
@click.argument('name')
def default(name):
    """Set a package as the default package."""
    try:
        modrc_package.set_default(name)
    except exceptions.ModRCIntegrityError:
        click.secho('ModRC is not installed', fg='red', bold=True)
        sys.exit(2)
    except exceptions.ModRCPackageDoesNotExistError:
        click.secho('Package {} does not exist'.format(name), fg='red', bold=True)
        sys.exit(2)
    click.echo("Package {} has been set as default".format(name))

@package.command(name='list')
def list_command():
    """List all installed packages."""
    # get all the installed packages
    try:
        packages = modrc_package.list_packages()
    except exceptions.ModRCIntegrityError:
        click.secho('ModRC is not installed', fg='red', bold=True)
        sys.exit(2)
    # print the packages to stdout
    click.echo('Packages')
    click.echo('--------')
    for p in packages:
        click.echo(p)
