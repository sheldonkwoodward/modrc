# ModRC CLI
![](https://github.com/sheldonkwoodward/modrc-cli/workflows/tests/badge.svg)
![](https://img.shields.io/github/license/sheldonkwoodward/modrc-cli.svg)

The command line interface for the ModRC shell profile management workflow. ModRC CLI makes it easy to install, manage, and sync your shell profile across all your computer.

# Installation
```
$ pip install .
```

# Commands
- manifest - Manage manifests
- package - Manage packages
- setup - Setup ModRC

## manifest
Manage manifests

### Synopsis
- `modrc manifest`
- `modrc manifest new [<name>]`
- `modrc manifest add <package>`

## package
Manage packages

### Synopsis
- `modrc package`
- `modrc package install <url>`
- `modrc package uninstall (<url> | <name>)`

## setup
Setup ModRC

### Synopsis
- `modrc setup [(-d | --directory) <directory>] [(-r | --repo) <url>] [--no-default]`
- `modrc setup directory [(-m | --move)] <directory>`
- `modrc setup repo set <url>`
- `modrc setup repo remove <url>`
