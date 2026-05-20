from inspect import signature

# Errors
from .errors import DefaultFormatModificationError, MissingStringError, InvalidArgumentError, FormatAlreadyExistsError, AliasAlreadyExistsError

class Formatter:
#--------(Format functions)--------
    @staticmethod
    def cap(s):
        """Capitalize the first character of the string and make the rest lowercase."""
        return s.capitalize()

    @staticmethod
    def up(s):
        """Convert all characters in the string to uppercase."""
        return s.upper()

    @staticmethod
    def down(s):
        """Convert all characters in the string to lowercase."""
        return s.lower()

    @staticmethod
    def spike(s):
        """Convert characters in the string to alternating uppercase and lowercase, starting with uppercase."""
        s = s.lower()
        return ''.join(
            char.upper() if i % 2 == 0 else char
            for i, char in enumerate(s))

    @staticmethod
    def clean(s):
        """Remove extra spaces from the string, leaving only single spaces between words."""
        words = s.split()
        return ' '.join(words)

    @staticmethod
    def camel_case(s):
        """Convert the string to camelCase."""
        words = s.lower().split()
        return words[0] + ''.join(
            word.capitalize()
            for word in words[1:])

    @staticmethod
    def snake_case(s):
        """Convert the string to snake_case."""
        words = s.lower().split()
        return '_'.join(words)

    @staticmethod
    def pascal_case(s):
        """Convert the string to PascalCase."""
        words = s.split()
        return ''.join(
            word.capitalize()
            for word in words)

    @staticmethod
    def upper_snake_case(s):
        """Convert the string to UPPER_SNAKE_CASE."""
        words = s.upper().split()
        return '_'.join(words)
    
    @staticmethod
    def no_spaces(s):
        """Remove all spaces from the string."""
        return s.replace(' ', '') 

#--------(Formats)--------

    formats = {
        "capitalize": cap,
        "up": up,
        "down": down,
        "spike": spike,
        "clean": clean,
        "camelCase": camel_case,
        "snake_case": snake_case,
        "PascalCase": pascal_case,
        "UPPER_SNAKE_CASE": upper_snake_case,
        "nospaces": no_spaces
    }

    default_formats = formats.copy()
    custom_formats = {}
    format_aliases = {}
    enabled_formats = list(formats.keys()) + list(format_aliases.keys())

#--------(Formatter function)--------
    @classmethod
    def get_callable(cls, string_format):
        if string_format in cls.format_aliases:
            func = cls.format_aliases[string_format]
        elif string_format in cls.formats:
            func = cls.formats[string_format]
        else:
            raise InvalidArgumentError(
                f"Invalid string format: '{string_format}'. "
                f"Expected one of: {', '.join(cls.formats)}."
            )

        if string_format not in cls.enabled_formats:
            raise InvalidArgumentError(
                f"Format '{string_format}' is currently disabled. "
                f"Enabled formats: {', '.join(cls.enabled_formats)}."
            )
        
        return func
#--------

#--------
    @classmethod
    def formatting(cls,
        string: str,
        string_format: str,
        inverse: bool = False,
        reverse: bool = False
    ) -> str:

        """
        Format string using specified formatting style.

        Args:
            string: Input string.
            string_format: Formatting style.
            inverse: Invert character case.
            reverse: Reverse output string.

        Returns:
            Formatted string.
        """
    
        string = cls._validate(string)

        func = cls.get_callable(string_format)

        output = func(string)

        if inverse:
            output = output.swapcase()

        if reverse:
            output = output[::-1]

        return output
#--------
    
#--------(Pipeline API)--------
    @classmethod
    def pipe(cls, string, *formats, inversed=False, reversed=False):
        """
        Apply multiple formats to a string in sequence.

        Args:
            string: Input string.
            *formats: Sequence of format names to apply.
        """
        
        for fmt in formats:
            string = cls.formatting(string, fmt, inverse=inversed, reverse=reversed)
        return string
#--------

#--------(Registry API)--------
    @classmethod
    def add_format(cls, func=None, name=None, *aliases):
        def decorator(f):
            cls.__validate_format_function(f)

            format_name = (
                name
                if name is not None
                else f.__name__
            )

            if cls.is_existing_format(format_name):
                raise FormatAlreadyExistsError(
                    f"Unable to add format: format '{format_name}' already exists."
                )
            
            if cls.is_existing_alias(format_name):
                raise AliasAlreadyExistsError(
                    f"Unable to add format: '{format_name}' is already an alias."
                )

            if format_name in list(cls.default_formats):
                raise DefaultFormatModificationError(
                    f"Unable to add format: '{format_name}' is a default format.")

            cls.formats[format_name] = f
            cls.custom_formats[format_name] = f
            cls.enabled_formats.append(format_name)

            if aliases:
                for alias in aliases:
                    if cls.is_existing_alias(alias):
                        raise AliasAlreadyExistsError(
                            f"Unable to add alias: alias '{alias}' already exists."
                        )
                    cls.format_aliases[alias] = f
                    cls.enabled_formats.append(alias)

            return f

        if func is None:
            return decorator
        
        return decorator(func)
#--------
    
#--------
    @classmethod
    def replace_format(cls, name, func):
        cls.__validate_format_function(func)

        if not cls.is_existing_format(name):
            raise InvalidArgumentError(
                f"Unable to replace format: format '{name}' does not exist."
            )

        if name in cls.default_formats:
            raise DefaultFormatModificationError(
                f"Unable to replace format: '{name}' is a default format."
            )

        cls.formats[name] = func
#--------

#--------
    @classmethod
    def remove_format(cls, name):
        if not cls.is_existing_format(name):
            raise InvalidArgumentError(
                f"Unable to remove format: format '{name}' does not exist or is alias."
            )

        cls.del_aliases_of(name)

        if name in cls.enabled_formats:
            cls.enabled_formats.remove(name)

        cls.formats.pop(name, None)
        cls.custom_formats.pop(name, None)
#--------

#--------
    @classmethod
    def reset_formats(cls):
        cls.clear_aliases()
        cls.clear_custom_formats()
        cls.formats = cls.default_formats.copy()
#--------

#--------
    @classmethod
    def restore_format(cls, name):
        if name not in cls.default_formats:
            raise InvalidArgumentError(
                f"Unable to restore format: format '{name}' is not a default format."
            )
        
        if name in cls.custom_formats:
            raise FormatAlreadyExistsError(
                f"Unable to restore format: format '{name}' already exists as a custom format."
            )

        cls.formats[name] = cls.default_formats[name]
        cls.custom_formats.pop(name, None)
        if name not in cls.enabled_formats:
            cls.enabled_formats.append(name)
#--------

#--------
    @classmethod
    def clear_formats(cls):
        cls.formats.clear()
        cls.custom_formats.clear()
        cls.enabled_formats.clear()
        cls.format_aliases.clear()
#--------

#--------
    @classmethod
    def clear_default_formats(cls):
        for name in list(cls.default_formats):
            cls.del_aliases_of(name)

            if name in cls.enabled_formats:
                cls.enabled_formats.remove(name)

            cls.formats.pop(name, None)
#--------

#--------
    @classmethod
    def clear_custom_formats(cls):
        for name in list(cls.custom_formats):
            cls.del_aliases_of(name)

            if name in cls.enabled_formats:
                cls.enabled_formats.remove(name)

            cls.formats.pop(name, None)

        cls.custom_formats.clear()
#--------

#--------
    @classmethod
    def get_formats(cls):
        return cls.formats
#--------
    
#--------
    @classmethod
    def get_default_formats(cls):
        return {
            name: cls.formats[name]
            for name in cls.formats
            if name in cls.default_formats
        }
#--------
    
#--------
    @classmethod
    def get_custom_formats(cls):
        return cls.custom_formats
#--------

#--------
    @classmethod
    def get_builtin_formats(cls):
        return cls.default_formats
#--------

#--------
    @classmethod
    def get_format_function(cls, name):
        if not cls.is_existing_format(name):
            raise InvalidArgumentError(
                f"Format '{name}' does not exist. Available formats: {', '.join(cls.formats)}."
            )

        return cls.formats[name]
#--------

#--------
    @classmethod
    def names_of(cls, func):
        names = []
        for name, f in cls.formats.items():
            if f is func:
                names.append(name)
        if names:
            return names
        raise InvalidArgumentError(
            f"Format {func.__name__} not found."
        )
#--------

#--------
    @classmethod
    def get_format_info(cls, name):
        if not cls.is_existing_format(name):
            raise InvalidArgumentError(
                f"Format '{name}' does not exist. "
                f"Available formats: {', '.join(cls.formats)}."
            )

        func = cls.formats[name]
        return {
            "name": name,
            "function": func,
            "doc": func.__doc__
        }
#--------

#--------
    @classmethod
    def get_format_doc(cls, name):
        return cls.get_format_function(name).__doc__
#--------

#--------
    @classmethod
    def rename_format(cls, old_name, new_name):
        if not cls.is_existing_format(old_name):
            raise InvalidArgumentError(
                f"Unable to rename format: format '{old_name}' does not exist."
            )

        if cls.is_existing_format(new_name):
            raise FormatAlreadyExistsError(
                f"Unable to rename format: format '{new_name}' already exists."
            )

        if cls.is_existing_alias(new_name):
            raise FormatAlreadyExistsError(
                f"Unable to rename format: alias '{new_name}' already exists."
            )
        
        if new_name in cls.default_formats:
            raise DefaultFormatModificationError(
                f"Unable to replace format: '{new_name}' is a default format."
            )

        aliases = list(cls.aliases_of(old_name))

        func = cls.formats.pop(old_name)

        cls.formats[new_name] = func

        if old_name in cls.custom_formats:
            cls.custom_formats[new_name] = cls.custom_formats.pop(old_name)

        if old_name in cls.enabled_formats:
            cls.enabled_formats.remove(old_name)
            cls.enabled_formats.append(new_name)

        for alias in aliases:
            cls.format_aliases[alias] = func
#--------

#--------
    @classmethod
    def has_format(cls, name):
        return cls.is_existing_format(name)
#--------

#--------
    @classmethod
    def has_alias(cls, name):
        return cls.is_existing_alias(name)
#--------

#--------
    @classmethod
    def disable(cls, name):
        if not cls.is_existing_format(name):
            raise InvalidArgumentError(
                f"Unable to disable format: format '{name}' does not exist."
            )

        aliases = list(cls.aliases_of(name))

        for alias in aliases:
            if alias in cls.enabled_formats:
                cls.enabled_formats.remove(alias)

        if name in cls.enabled_formats:
            cls.enabled_formats.remove(name)
#--------

#--------
    @classmethod
    def enable(cls, name):
        if not cls.is_existing_format(name):
            raise InvalidArgumentError(
                f"Unable to enable format: format '{name}' does not exist."
            )

        aliases = list(cls.aliases_of(name))
        if not cls.is_enabled(name):
            cls.enabled_formats.append(name)
        for alias in aliases:
            if not cls.is_enabled(alias):
                cls.enabled_formats.append(alias)
#--------

#--------
    @classmethod
    def toggle(cls, name):
        if not cls.is_existing_format(name):
            raise InvalidArgumentError(
                f"Unable to toggle format: format '{name}' does not exist."
            )
        
        aliases = list(cls.aliases_of(name))
        if cls.is_enabled(name):
            cls.enabled_formats.remove(name)

            for alias in aliases:
                if alias in cls.enabled_formats:
                    cls.enabled_formats.remove(alias)
        else:
            cls.enabled_formats.append(name)

            for alias in aliases:
                if alias not in cls.enabled_formats:
                    cls.enabled_formats.append(alias)
#--------

#--------
    @classmethod
    def is_enabled(cls, name):
        return name in cls.enabled_formats
#--------

#--------(Validation API)--------
    @classmethod
    def _validate(cls, s):
        s = s.strip()
        if not s:
            raise MissingStringError(
                "Input string is empty or contains only whitespace."
            )
        return s
#--------

#--------
    @classmethod
    def is_existing_format(cls, name):
        return name in cls.formats
#--------
 
#--------    
    @classmethod
    def is_existing_alias(cls, name):
        return name in cls.format_aliases
#--------

#--------
    @classmethod
    def __validate_format_function(cls, func):
        sig = signature(func)

        if len(sig.parameters) != 1:
            raise InvalidArgumentError("Format function must accept exactly one argument.")
#--------

#--------(Alias API)--------

    @classmethod
    def alias(cls, existing_name, alias_name):
        if not cls.is_existing_format(existing_name):
            raise InvalidArgumentError(
                f"Unable to create alias: format '{existing_name}' does not exist."
            )

        if cls.is_existing_alias(alias_name):
            temp = cls.format_aliases[alias_name]
            format_name = next(
                n
                for n, f in cls.formats.items()
                if f is temp
            )
            raise AliasAlreadyExistsError(
                f"Unable to create alias: alias '{alias_name}' already exists for format '{format_name}'."
            )

        cls.format_aliases[alias_name] = cls.formats[existing_name]

        if alias_name not in cls.enabled_formats:
            cls.enabled_formats.append(alias_name)
#--------

#--------
    @classmethod
    def del_alias(cls, alias_name):
        if not cls.is_existing_alias(alias_name):
            raise InvalidArgumentError(
                f"Unable to delete alias: alias '{alias_name}' does not exist."
            )

        if alias_name in cls.enabled_formats:
            cls.enabled_formats.remove(alias_name)

        del cls.format_aliases[alias_name]
#--------

#--------
    @classmethod
    def del_aliases_of(cls, existing_name):
        if not cls.is_existing_format(existing_name):
            raise InvalidArgumentError(
                f"Unable to delete alias: format '{existing_name}' does not exist."
            )

        aliases_to_delete = [
            name
            for name, func in cls.format_aliases.items()
            if func is cls.formats[existing_name]
        ]

        for alias in aliases_to_delete:
            if alias in cls.enabled_formats:
                cls.enabled_formats.remove(alias)

            del cls.format_aliases[alias]
#--------

#--------
    @classmethod
    def clear_aliases(cls):
        for alias in list(cls.format_aliases):
            if alias in cls.enabled_formats:
                cls.enabled_formats.remove(alias)
            del cls.format_aliases[alias]
#--------

#--------
    @classmethod
    def aliases_of(cls, existing_name):
        if not cls.is_existing_format(existing_name):
            raise InvalidArgumentError(
                f"Unable to list aliases: format '{existing_name}' does not exist."
            )

        return {
            name: func
            for name, func in cls.format_aliases.items()
            if func is cls.formats[existing_name] and name != existing_name
        }
#--------

#--------
    @classmethod
    def get_all_aliases(cls):
        return cls.format_aliases
#--------