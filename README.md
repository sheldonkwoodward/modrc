# modrc
[![PyPI Version](https://img.shields.io/pypi/v/modrc)](https://pypi.org/project/modrc/)
[![PyPI Status](https://img.shields.io/pypi/status/modrc)](https://pypi.org/project/modrc/)
[![License](https://img.shields.io/github/license/sheldonkwoodward/modrc.svg)](https://github.com/sheldonkwoodward/modrc/blob/master/LICENSE.txt)
[![Tests Status](https://github.com/sheldonkwoodward/modrc-cli/workflows/tests/badge.svg)]()
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/22a052d84a1f437e93e2364710a1f911)](https://www.codacy.com/manual/sheldonkwoodward/modrc?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=sheldonkwoodward/modrc&amp;utm_campaign=Badge_Grade)

The CLI to make managing your config files across systems easier.

## Description
ModRC makes it easy to install, manage, and sync your dotfiles or any other config across all your computers.

## Installation
Installation of ModRC is easy, install it directly from PyPI.
```
$ pip install modrc
```

If you want to edit the installed code or PyPI is not available, setuptools works for installation.
```
$ pip install -e .
```

After installing with pip, run the installation command.
```
$ modrc setup install
```

This will create the ModRC directory at `~/.modrc`.

## Usage
ModRC consists of a number of sub-commands to manage your installatio and files. **Not all commands are available/working as this project is still in Alpha.** This list acts as a guideline for development, not an official list of forthcoming commands.

### Setup
```
modrc setup
modrc setup install [(-e|--editor) <editor>] [(-u|--url) <url>] [(-p|--package) <package>] [(-c|--compile)] [(-s|--auto-sync)]
modrc setup uninstall
```

### Compile
```
modrc compile [--package <package> [--file <file>]]
```

### Package
```
modrc package add [(-d | --default)] [--url <url>] <package>
modrc package remove [-y] <package>
modrc package edit [<package>]
modrc package default <package>
modrc package sync [<package>]
```

### File
```
modrc file add <file> [<package>]
modrc file remove [-y] <file> [<package>]
modrc file edit [((-c|--compile)|(-n|--no-compile))] <file> [<package>]
```

### Filter
```
modrc filter add <filter> <file> [<package>]
modrc filter remove [-y] <filter> <file> [<package>]
modrc filter edit <filter> <file> [<package>]
```

### Chunk
```
modrc chunk add <chunk> [<package>]
modrc chunk remove [-y] <chunk> [<package>]
modrc chunk edit <chunk> [<package>]
```

## Testing
Testing is slightly complicated since ModRC creates and deletes files in a user's home directory. To avoid modifying files in your home directory, it is advised to run the tests in a container. To run the tests in an isolated Docker container, use the following command. It will mount the code as a volume so you dont have to re-compile the container every time the tests run.
```
$ ./run_tests.sh
```
