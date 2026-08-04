"""
NexPro Professional Lexer
Version 0.3.0
"""

from nexpro.tokens import (
    Token,
    SAY,
    IDENTIFIER,
    STRING,
    NUMBER,
    ASSIGN,
    PLUS,
    MINUS,
    STAR,
    SLASH,
    LPAREN,
    RPAREN,
    EOF,
)
from nexpro.errors import NexProSyntaxError

class Lexer:

    def __init__(self, source):

        self.source = source

        self.position = 0

        self.line = 1

        self.column = 1

        self.current = self.source[0] if self.source else None

    # -------------------------

    def advance(self):

        if self.current == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        self.position += 1

        if self.position >= len(self.source):
            self.current = None
        else:
            self.current = self.source[self.position]

    # -------------------------

    def skip_whitespace(self):

        while self.current and self.current.isspace():
            self.advance()

    # -------------------------

    def identifier(self):

        start_col = self.column

        value = ""

        while self.current and (
            self.current.isalnum()
            or self.current == "_"
        ):
            value += self.current
            self.advance()

        if value == "say":
            return Token(
                SAY,
                value,
                self.line,
                start_col
            )

        return Token(
            IDENTIFIER,
            value,
            self.line,
            start_col
        )

    # -------------------------

    def number(self):

        start_col = self.column

        value = ""

        while self.current and self.current.isdigit():

            value += self.current

            self.advance()

        return Token(
            NUMBER,
            int(value),
            self.line,
            start_col
        )

    # -------------------------

    def string(self):

        start_col = self.column

        self.advance()

        value = ""

        while self.current != '"':

            if self.current is None:
                raise NexProSyntaxError(
                    "Unknown statement",
                    line=self.line,
                    column=self.column,
                    filename=self.current.filename if hasattr(self.current, 'filename') else None,
                )

            value += self.current

            self.advance()

        self.advance()

        return Token(
            STRING,
            value,
            self.line,
            start_col
        )

    # -------------------------

    def tokenize(self):

        tokens = []

        while self.current:

            if self.current.isspace():
                self.skip_whitespace()
                continue

            if self.current.isalpha() or self.current == "_":
                tokens.append(self.identifier())
                continue

            if self.current.isdigit():
                tokens.append(self.number())
                continue

            if self.current == '"':
                tokens.append(self.string())
                continue

            if self.current == "=":
                tokens.append(
                    Token(
                        ASSIGN,
                        "=",
                        self.line,
                        self.column,
                    )
                )
                self.advance()
                continue

            if self.current == "+":
                tokens.append(
                    Token(
                        PLUS,
                        "+",
                        self.line,
                        self.column,
                    )
                )
                self.advance()
                continue

            if self.current == "-":
                tokens.append(
                    Token(
                        MINUS,
                        "-",
                        self.line,
                        self.column,
                    )
                )
                self.advance()
                continue

            if self.current == "*":
                tokens.append(
                    Token(
                        STAR,
                        "*",
                        self.line,
                        self.column,
                    )
                )
                self.advance()
                continue

            if self.current == "/":
                tokens.append(
                    Token(
                        SLASH,
                        "/",
                        self.line,
                        self.column,
                    )
                )
                self.advance()
                continue

            if self.current == "(":
                tokens.append(
                    Token(
                        LPAREN,
                        "(",
                        self.line,
                        self.column,
                    )
                )
                self.advance()
                continue

            if self.current == ")":
                tokens.append(
                    Token(
                        RPAREN,
                        ")",
                        self.line,
                        self.column,
                    )
                )
                self.advance()
                continue

            raise SyntaxError(
                f"Unexpected character '{self.current}' at "
                f"{self.line}:{self.column}"
            )

        tokens.append(
            Token(
                EOF,
                "",
                self.line,
                self.column,
            )
        )

        return tokens