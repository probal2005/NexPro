"""Language diagnostics for NexPro."""


class NexProError(Exception):
    """Base class for all NexPro errors."""


class SourceError(NexProError):
    """An error with a source location and an optional excerpt."""

    stage = "Source"

    def __init__(self, message, line=0, column=0, filename=None):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column
        self.filename = filename
        self.source_line = None

    def locate(self, source):
        lines = source.split("\n")
        if 1 <= self.line <= len(lines):
            self.source_line = lines[self.line - 1]

    def __str__(self):
        rule = "=" * 50
        text = [rule, f" NexPro {self.stage} Error", rule]
        if self.filename:
            text.append(f"File   : {self.filename}")
        text.extend([f"Line   : {self.line}", f"Column : {self.column}", "", self.message])
        if self.source_line is not None:
            prefix = self.source_line[:max(0, self.column - 1)].expandtabs(4)
            text.extend(["", self.source_line.expandtabs(4), " " * len(prefix) + "^"])
        text.append(rule)
        return "\n".join(text)


class LexerError(SourceError):
    stage = "Lexer"


class ParserError(SourceError):
    stage = "Parser"


class ImportError(SourceError):
    stage = "Import"


EXECUTION_ERRORS = (ArithmeticError, TypeError, ValueError, RecursionError, IndexError, KeyError, EOFError)


class RuntimeError(NexProError):
    def __init__(self, message, code="runtime_error", details=None):
        super().__init__(message)
        self.code = code
        self.details = details
        self.message = message
        self.frames = []

    def add_frame(self, function, location):
        if location is not None:
            self.frames.append((function, *location))

    def __str__(self):
        lines = [f"NexPro Runtime Error: {self.message}"]
        lines.extend(f"  at {function} ({filename}:{line})" for function, filename, line in self.frames)
        return "\n".join(lines)
