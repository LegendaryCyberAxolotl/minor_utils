class InvalidArgumentError(ValueError):
    pass

class MissingStringError(ValueError):
    pass

class FormatAlreadyExistsError(Exception):
    pass

class AliasAlreadyExistsError(FormatAlreadyExistsError):
    pass

class DefaultFormatModificationError(Exception):
    pass