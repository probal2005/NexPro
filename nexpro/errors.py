"""
NexPro Error System
Version 0.3.0
"""


class NexProError(Exception):
    """Base class for all NexPro errors."""
    pass


class NexProSyntaxError(NexProError):

    def __init__(self, message, line=None, column=None, filename=None):

        self.message = message
        self.line = line
        self.column = column
        self.filename = filename

        super().__init__(message)

    def __str__(self):

        text = []

        text.append("=" * 40)
        text.append(" NexPro Syntax Error")
        text.append("=" * 40)

        if self.filename:
            text.append(f"File   : {self.filename}")

        if self.line is not None:
            text.append(f"Line   : {self.line}")

        if self.column is not None:
            text.append(f"Column : {self.column}")

        text.append("")
        text.append(self.message)
        text.append("")
        text.append("=" * 40)

        return "\n".join(text)