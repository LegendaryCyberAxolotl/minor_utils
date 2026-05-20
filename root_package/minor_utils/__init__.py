__title__ = "minor_utils"
__version__ = "0.1.0"
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