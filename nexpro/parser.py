"""
NexPro Programming Language
Parser
Version 0.5.0
Author: Probal Dhali
"""

from nexpro.tokens import EOF
from nexpro.ast import Program
from nexpro.errors import ParserError


class Parser:

    def __init__(self, tokens):

        self.tokens = tokens
        self.position = 0
        self.current = self.tokens[0]

    # =========================================================

    def advance(self):
        """
        Move to next token.
        """

        if self.position < len(self.tokens) - 1:

            self.position += 1
            self.current = self.tokens[self.position]

        return self.current

    # =========================================================

    def previous(self):
        """
        Return previous token.
        """

        if self.position == 0:
            return None

        return self.tokens[self.position - 1]

    # =========================================================

    def peek(self):
        """
        Look ahead one token.
        """

        if self.position + 1 >= len(self.tokens):
            return None

        return self.tokens[self.position + 1]

    # =========================================================

    def is_end(self):

        return self.current.type == EOF

    # =========================================================

    def check(self, token_type):
        """
        Check current token without consuming it.
        """

        if self.is_end():
            return False

        return self.current.type == token_type

    # =========================================================

    def match(self, *types):
        """
        Match one of many token types.
        """

        for token_type in types:

            if self.check(token_type):

                self.advance()

                return True

        return False

    # =========================================================

    def expect(self, token_type, message="Unexpected token"):
        """
        Consume required token.
        """

        if self.check(token_type):

            token = self.current

            self.advance()

            return token

        raise ParserError(
            message,
            line=self.current.line,
            column=self.current.column,
        )

    # =========================================================

    def statement(self):

        self.advance()

        return None

    # =========================================================

    def parse(self):

        statements = []

        while not self.is_end():

            node = self.statement()

            if node is not None:
                statements.append(node)

        return Program(statements)