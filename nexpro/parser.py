"""
NexPro Programming Language
Parser
Version 0.5.0
Author: Probal Dhali
"""

from nexpro.tokens import EOF
from nexpro.ast import Program


class Parser:

    def __init__(self, tokens):

        self.tokens = tokens
        self.position = 0
        self.current = self.tokens[0]

    # =====================================================

    def advance(self):

        if self.position < len(self.tokens) - 1:

            self.position += 1
            self.current = self.tokens[self.position]

    # =====================================================

    def peek(self):

        if self.position + 1 >= len(self.tokens):
            return None

        return self.tokens[self.position + 1]

    # =====================================================

    def is_end(self):

        return self.current.type == EOF

    # =====================================================

    def statement(self):

        """
        Placeholder.

        In Lesson 6 this will parse:

        say

        assignment

        if

        while

        repeat
        """

        self.advance()

        return None

    # =====================================================

    def parse(self):

        statements = []

        while not self.is_end():

            node = self.statement()

            if node is not None:
                statements.append(node)

        return Program(statements)