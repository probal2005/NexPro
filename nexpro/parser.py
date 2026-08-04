"""
NexPro Parser
Version 0.3.0
"""

from nexpro.tokens import (
    IDENTIFIER,
    STRING,
    NUMBER,
    ASSIGN,
    SAY,
    PLUS,
    MINUS,
    STAR,
    SLASH,
    LPAREN,
    RPAREN,
    EOF,
)

from nexpro.ast import (
    Program,
    Assign,
    Variable,
    String,
    Number,
    Say,
    Binary,
)


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current = self.tokens[0]

    # ---------------------------------

    def advance(self):
        self.position += 1

        if self.position < len(self.tokens):
            self.current = self.tokens[self.position]

    # ---------------------------------

    def expect(self, token_type):

        if self.current.type != token_type:
            raise SyntaxError(
                f"Expected {token_type}, got {self.current.type}"
            )

        token = self.current
        self.advance()

        return token

    # ---------------------------------

    def factor(self):

        token = self.current

        if token.type == STRING:
            self.advance()
            return String(token.value)

        if token.type == NUMBER:
            self.advance()
            return Number(token.value)

        if token.type == IDENTIFIER:
            self.advance()
            return Variable(token.value)

        if token.type == LPAREN:
            self.advance()

            node = self.expression()

            self.expect(RPAREN)

            return node

        raise SyntaxError(
            f"Unexpected token {token.type}"
        )

    # ---------------------------------

    def term(self):

        node = self.factor()

        while self.current.type in (
            STAR,
            SLASH,
        ):

            operator = self.current.value

            self.advance()

            node = Binary(
                node,
                operator,
                self.factor(),
            )

        return node

    # ---------------------------------

    def expression(self):

        node = self.term()

        while self.current.type in (
            PLUS,
            MINUS,
        ):

            operator = self.current.value

            self.advance()

            node = Binary(
                node,
                operator,
                self.term(),
            )

        return node

    # ---------------------------------

    def assignment(self):

        name = self.expect(IDENTIFIER)

        self.expect(ASSIGN)

        value = self.expression()

        return Assign(
            Variable(name.value),
            value,
        )

    # ---------------------------------

    def say_statement(self):

        self.expect(SAY)

        value = self.expression()

        return Say(value)

    # ---------------------------------

    def statement(self):

        if self.current.type == SAY:
            return self.say_statement()

        if self.current.type == IDENTIFIER:
            return self.assignment()

        raise SyntaxError(
            f"Unexpected statement {self.current.type}"
        )

    # ---------------------------------

    def parse(self):

        statements = []

        while self.current.type != EOF:
            statements.append(
                self.statement()
            )

        return Program(statements)