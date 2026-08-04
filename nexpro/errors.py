"""
NexPro Programming Language
Error System
Version 0.4.0
Author: Probal Dhali
"""


class NexProError(Exception):
    """Base class for all NexPro errors."""
    pass


# ==========================================================
# Lexer Error
# ==========================================================

class LexerError(NexProError):

    def __init__(self, message, line=0, column=0, filename=None):
        self.message = message
        self.line = line
        self.column = column
        self.filename = filename

        super().__init__(message)

    def __str__(self):

        text = []

        text.append("=" * 50)
        text.append(" NexPro Lexer Error")
        text.append("=" * 50)

        if self.filename:
            text.append(f"File   : {self.filename}")

        text.append(f"Line   : {self.line}")
        text.append(f"Column : {self.column}")

        text.append("")
        text.append(self.message)
        text.append("=" * 50)

        return "\n".join(text)


# ==========================================================
# Parser Error
# ==========================================================

class ParserError(NexProError):

    def __init__(self, message, line=0, column=0, filename=None):
        self.message = message
        self.line = line
        self.column = column
        self.filename = filename

        super().__init__(message)

    def __str__(self):

        text = []

        text.append("=" * 50)
        text.append(" NexPro Parser Error")
        text.append("=" * 50)

        if self.filename:
            text.append(f"File   : {self.filename}")

        text.append(f"Line   : {self.line}")
        text.append(f"Column : {self.column}")

        text.append("")
        text.append(self.message)
        text.append("=" * 50)

        return "\n".join(text)


# ==========================================================
# Runtime Error
# ==========================================================

class RuntimeError(NexProError):

    def __init__(self, message):
        self.message = message

        super().__init__(message)

    def __str__(self):

        text = []

        text.append("=" * 50)
        text.append(" NexPro Runtime Error")
        text.append("=" * 50)
        text.append("")
        text.append(self.message)
        text.append("=" * 50)

        return "\n".join(text)