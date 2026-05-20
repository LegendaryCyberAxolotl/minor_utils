from importlib.metadata import version

__title__ = "minor_utils"
__version__ = version("minor_utils")
__author__ = "Gleb Minor"
__license__ = "MIT"

from .formatter import Formatter
from .func_manager import Manager
from .errors import MissingStringError, InvalidArgumentError, FormatAlreadyExistsError, AliasAlreadyExistsError, DefaultFormatModificationError

__all__ = [
    "Formatter",
    "Manager",
    "MissingStringError",
    "InvalidArgumentError",
    "FormatAlreadyExistsError",
    "AliasAlreadyExistsError",
    "DefaultFormatModificationError"
]