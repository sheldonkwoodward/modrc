# sheldon woodward
# 4/15/18

"""Main CLI entrypoint."""

from .commands import *


@click.group()
def main():
    pass


# commands
main.add_command(ping)


if __name__ == '__main__':
    main()
