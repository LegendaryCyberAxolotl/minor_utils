# Errors
from .errors import MissingStringError, InvalidArgumentError

class Formatter:
    
#--------(String validation)--------
    @staticmethod
    def _validate(s):
        s = s.strip()
        if not s:
            raise MissingStringError(
                "Input string is empty or contains only whitespace."
            )
        return s

#--------(Format functions)--------

    @staticmethod
    def cap(s):
        return s.capitalize()

    @staticmethod
    def up(s):
        return s.upper()

    @staticmethod
    def down(s):
        return s.lower()

    @staticmethod
    def spike(s):
        s = s.lower()
        return ''.join(
            char.upper() if i % 2 == 0 else char
            for i, char in enumerate(s))

    @staticmethod
    def clean(s):
        words = s.split()
        return ' '.join(words)

    @staticmethod
    def camel_case(s):
        words = s.lower().split()
        return words[0] + ''.join(
            word.capitalize()
            for word in words[1:])

    @staticmethod
    def snake_case(s):
        words = s.lower().split()
        return '_'.join(words)

    @staticmethod
    def pascal_case(s):
        words = s.split()
        return ''.join(
            word.capitalize()
            for word in words)

    @staticmethod
    def upper_snake_case(s):
        words = s.upper().split()
        return '_'.join(words)

#--------(Formats)--------

    formats = {
        "capitalize": cap,
        "up": up,
        "down": down,
        "spike": spike,
        "clean": clean,
        "camel_case": camel_case,
        "snake_case": snake_case,
        "pascal_case": pascal_case,
        "upper_snake_case": upper_snake_case,
    }

#--------(Formatter function)--------

    @staticmethod
    def formatting(
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
    
        string = Formatter._validate(string)

        if string_format not in Formatter.formats:
            raise InvalidArgumentError(
                f"Invalid string format: '{string_format}'. "
                f"Expected one of: {', '.join(Formatter.formats)}."
            )

        output = Formatter.formats[string_format](string)

        if inverse:
            output = output.swapcase()

        if reverse:
            output = output[::-1]

        return output

    
