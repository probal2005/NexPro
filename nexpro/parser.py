"""
NexPro Parser
Version 0.5.0
Author: Probal Dhali
"""

from nexpro.tokens import EOF


class Parser:

    def __init__(self, tokens):

        self.tokens = tokens
        self.position = 0
        self.current = self.tokens[0]

    def advance(self):

        if self.position < len(self.tokens) - 1:

            self.position += 1
            self.current = self.tokens[self.position]

    def peek(self):

        if self.position + 1 >= len(self.tokens):
            return None

        return self.tokens[self.position + 1]

    def is_end(self):

        return self.current.type == EOF