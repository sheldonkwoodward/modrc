# base errors
class ModRCError(Exception):
    """Base class for ModRC errors."""
    pass


class CompileError(ModRCError):
    """Base class for compile errors."""
    pass


# compile errors
class FilterNameError(CompileError):
    """Raised when there is an invalid filter name"""
    pass
