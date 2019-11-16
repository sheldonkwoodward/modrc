# ModRC
![](https://github.com/sheldonkwoodward/modrc-cli/workflows/tests/badge.svg)
![](https://img.shields.io/github/license/sheldonkwoodward/modrc-cli.svg)

The CLI to make managing your config files across systems easier.


## Description
ModRC makes it easy to install, manage, and sync your dotfiles or any other config across all your computers.


## Installation
Installation of ModRC is easy, simply clone the repository and install with pip.
```
$ pip install .
```

After installing with pip, run the installation command.
```
$ modrc setup install
```

This will create the ModRC directory at `~/.modrc`.


## Usage
ModRC consists of a number of sub-commands to manage your installatio and files.

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
modrc file edit <file> [<package>]
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
