# base errors
class ModRCError(Exception):
    """Base class for ModRC errors."""


class ModRCInstalledError(ModRCError):
    """Raised when ModRC is already installed."""


class ModRCIntegrityError(ModRCError):
    """Raised when there is an error with the ModRC installation."""


class ModRCPackageExistsError(ModRCError):
    """Raised when a package already exists."""


class ModRCPackageDoesNotExistError(ModRCError):
    """Raised when a package does not exist."""


class ModRCFileExistsError(ModRCError):
    """Raised when a file already exists."""


class ModRCFileDoesNotExistError(ModRCError):
    """Raised when a file directory does not exist."""


class ModRCLiveFileDoesNotExistError(ModRCError):
    """Raised when a live file does not exist."""


class ModRCFilterDoesNotExistError(ModRCError):
    """Raised when a file is compiled when no filters exist for it."""


class ModRCFilterNameError(ModRCError):
    """Raised when there is an invalid filter name"""
