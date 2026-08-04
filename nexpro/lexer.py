"""
NexPro Programming Language
Lexer
Version 0.4.0
Author: Probal Dhali
"""

from nexpro.tokens import (
    Token,
    EOF,
    IDENTIFIER,
    NUMBER,
    SAY,
    IF,
    ELSE,
    END,
    REPEAT,
    WHILE,
    TRUE,
    FALSE,
    AND,
    OR,
    NOT,
    KEYWORDS,
    ASSIGN,

PLUS,
MINUS,
STAR,
SLASH,
MODULO,

EQUAL,
NOT_EQUAL,

LESS,
LESS_EQUAL,

GREATER,
GREATER_EQUAL,

LPAREN,
RPAREN,

LBRACE,
RBRACE,

LBRACKET,
RBRACKET,

COMMA,
DOT,
COLON,
SEMICOLON,

STRING,
)

from nexpro.errors import LexerError


class Lexer:

    def __init__(self, source, filename="<stdin>"):

        self.source = source
        self.filename = filename

        self.position = 0
        self.line = 1
        self.column = 1

        self.current = source[0] if source else None

    # =================================================

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

    # =================================================

    def peek(self):

        nxt = self.position + 1

        if nxt >= len(self.source):
            return None

        return self.source[nxt]

    # =================================================

    def is_end(self):

        return self.current is None

    # =================================================

    def error(self, message):

        raise LexerError(
            message,
            line=self.line,
            column=self.column,
            filename=self.filename,
        )

    # =================================================

    def skip_whitespace(self):

        while (
            self.current is not None
            and self.current in " \t\r\n"
        ):
            self.advance()

    # =================================================

    def skip_comment(self):

        while (
            self.current is not None
            and self.current != "\n"
        ):
            self.advance()

    # =================================================

    def make_token(self, token_type, value):

        return Token(
            token_type,
            value,
            self.line,
            self.column,
        )

    # =================================================

    def is_alpha(self, char):

        return char.isalpha() or char == "_"

    # =================================================

    def is_digit(self, char):

        return char.isdigit()

    # =================================================

    def is_alnum(self, char):

        return char.isalnum() or char == "_"

    # =================================================

    def identifier(self):

        start_line = self.line
        start_column = self.column

        text = ""

        while (
            self.current is not None
            and self.is_alnum(self.current)
        ):
            text += self.current
            self.advance()

        token_type = KEYWORDS.get(
            text,
            IDENTIFIER,
        )

        return Token(
            token_type,
            text,
            start_line,
            start_column,
        )

    # =================================================

    def number(self):

        start_line = self.line
        start_column = self.column

        text = ""
        decimal_found = False

        while self.current is not None:

            if self.current.isdigit():

                text += self.current
                self.advance()

            elif self.current == ".":

                if decimal_found:
                    break

                decimal_found = True

                text += self.current
                self.advance()

            else:
                break

        if decimal_found:
            value = float(text)
        else:
            value = int(text)

        return Token(
            NUMBER,
            value,
            start_line,
            start_column,
        )

    # =================================================

    def tokenize(self):

        tokens = []

        while self.current is not None:

            # Skip whitespace
            if self.current in " \t\r\n":
                self.skip_whitespace()
                continue

            # Skip comments
            if self.current == "#":
                self.skip_comment()
                continue

            # Identifier / Keyword
            if self.is_alpha(self.current):
                tokens.append(
                    self.identifier()
                )
                continue

            # Number
            if self.current.isdigit():
                tokens.append(
                    self.number()
                )
                continue

            # Unknown Character
            self.error(
                f"Unknown character '{self.current}'"
            )

            if self.current in ('"', "'"):

                tokens.append(
                    self.string()
                )
                continue

            # Operators & Symbols

            if self.current in "=!<>+-*/%(){}[],.:;":

                tokens.append(
                self.operator()
                )

                continue

        tokens.append(
            Token(
                EOF,
                None,
                self.line,
                self.column,
            )
        )

        return tokens

        # =================================================

    def string(self):

        start_line = self.line
        start_column = self.column

        quote = self.current

        self.advance()

        value = ""

        while self.current is not None and self.current != quote:

            if self.current == "\\":

                self.advance()

                if self.current is None:
                    self.error("Unterminated escape sequence")

                escapes = {
                    "n": "\n",
                    "t": "\t",
                    '"': '"',
                    "'": "'",
                    "\\": "\\",
                }

                value += escapes.get(
                    self.current,
                    self.current,
                )

            else:

                value += self.current

            self.advance()

        if self.current != quote:

            self.error("Unterminated string")

        self.advance()

        return Token(
            STRING,
            value,
            start_line,
            start_column,
        )


        # =================================================

    def operator(self):

        line = self.line
        column = self.column

        ch = self.current

        # = ==
        if ch == "=":

            if self.peek() == "=":

                self.advance()
                self.advance()

                return Token(EQUAL, "==", line, column)

            self.advance()
            return Token(ASSIGN, "=", line, column)

        # !=
        if ch == "!":

            if self.peek() == "=":

                self.advance()
                self.advance()

                return Token(NOT_EQUAL, "!=", line, column)

            self.error("Unexpected character '!'")

        # <

        if ch == "<":

            if self.peek() == "=":

                self.advance()
                self.advance()

                return Token(LESS_EQUAL, "<=", line, column)

            self.advance()
            return Token(LESS, "<", line, column)

        # >

        if ch == ">":

            if self.peek() == "=":

                self.advance()
                self.advance()

                return Token(GREATER_EQUAL, ">=", line, column)

            self.advance()
            return Token(GREATER, ">", line, column)

        # +

        if ch == "+":
            self.advance()
            return Token(PLUS, "+", line, column)

        # -

        if ch == "-":
            self.advance()
            return Token(MINUS, "-", line, column)

        # *

        if ch == "*":
            self.advance()
            return Token(STAR, "*", line, column)

        # /

        if ch == "/":
            self.advance()
            return Token(SLASH, "/", line, column)

        # %

        if ch == "%":
            self.advance()
            return Token(MODULO, "%", line, column)

        # (

        if ch == "(":
            self.advance()
            return Token(LPAREN, "(", line, column)

        # )

        if ch == ")":
            self.advance()
            return Token(RPAREN, ")", line, column)

        # {

        if ch == "{":
            self.advance()
            return Token(LBRACE, "{", line, column)

        # }

        if ch == "}":
            self.advance()
            return Token(RBRACE, "}", line, column)

        # [

        if ch == "[":
            self.advance()
            return Token(LBRACKET, "[", line, column)

        # ]

        if ch == "]":
            self.advance()
            return Token(RBRACKET, "]", line, column)

        # ,

        if ch == ",":
            self.advance()
            return Token(COMMA, ",", line, column)

        # .

        if ch == ".":
            self.advance()
            return Token(DOT, ".", line, column)

        # :

        if ch == ":":
            self.advance()
            return Token(COLON, ":", line, column)

        # ;

        if ch == ";":
            self.advance()
            return Token(SEMICOLON, ";", line, column)

        self.error(f"Unknown operator '{ch}'")


        # =================================================

    def scan_token(self):

        # Skip whitespace
        if self.current in " \t\r\n":
            self.skip_whitespace()
            return None

        # Skip comments
        if self.current == "#":
            self.skip_comment()
            return None

        # Identifier / Keyword
        if self.is_alpha(self.current):
            return self.identifier()

        # Number
        if self.current.isdigit():
            return self.number()

        # String
        if self.current in ('"', "'"):
            return self.string()

        # Operators
        if self.current in "=!<>+-*/%(){}[],.:;":
            return self.operator()

        self.error(
            f"Unknown character '{self.current}'"
        )


        # =================================================

    def tokenize(self):

        tokens = []

        while not self.is_end():

            token = self.scan_token()

            if token is not None:
                tokens.append(token)

        tokens.append(

            Token(
                EOF,
                None,
                self.line,
                self.column,
            )

        )

        return tokens