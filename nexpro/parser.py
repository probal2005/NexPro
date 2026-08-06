"""
NexPro Programming Language
Parser
Version 0.5.0
Package 2 - Lesson 2
Author: Probal Dhali
"""

from nexpro.tokens import (
    EOF,
    IDENTIFIER,
    STRING,
    NUMBER,
    ASSIGN,
    SAY,
    PLUS,
    MINUS,
    STAR,
    SLASH,
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

from nexpro.errors import ParserError


class Parser:

    def __init__(self, tokens):

        self.tokens = tokens
        self.position = 0
        self.current = self.tokens[0]

    # ==========================================================
    # Navigation
    # ==========================================================

    def advance(self):
        """Move to next token."""

        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current = self.tokens[self.position]

        return self.current

    # ==========================================================

    def previous(self):
        """Return previous token."""

        if self.position == 0:
            return None

        return self.tokens[self.position - 1]

    # ==========================================================

    def peek(self):
        """Look ahead one token."""

        if self.position + 1 >= len(self.tokens):
            return None

        return self.tokens[self.position + 1]

    # ==========================================================

    def is_end(self):

        return self.current.type == EOF

    # ==========================================================

    def check(self, token_type):

        if self.is_end():
            return False

        return self.current.type == token_type

    # ==========================================================

    def match(self, *types):

        for token_type in types:

            if self.check(token_type):

                self.advance()

                return True

        return False

    # ==========================================================

    def expect(self, token_type, message="Unexpected token"):

        if self.check(token_type):

            token = self.current

            self.advance()

            return token

        raise ParserError(
            message,
            line=self.current.line,
            column=self.current.column,
        )

    # ==========================================================
    # Primary Expressions
    # ==========================================================

    def primary(self):

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

        raise ParserError(
            "Expected expression",
            line=token.line,
            column=token.column,
        )

    # ==========================================================
    # Expression
    # ==========================================================

    def expression(self):

        return self.addition()

    # ==========================================================
    # Assignment
    # ==========================================================

    def assignment(self):

        name = self.expect(
            IDENTIFIER,
            "Expected variable name",
        )

        self.expect(
            ASSIGN,
            "Expected '='",
        )

        value = self.expression()

        return Assign(
            Variable(name.value),
            value,
        )

    # ==========================================================
    # Say Statement
    # ==========================================================

    def say_statement(self):

        self.expect(
            SAY,
            "Expected 'say'",
        )

        value = self.expression()

        return Say(value)

    # ==========================================================
    # Statement
    # ==========================================================

    def statement(self):

        if self.check(SAY):
            return self.say_statement()

        if self.check(IDENTIFIER):
            return self.assignment()

        raise ParserError(
            "Unknown statement",
            line=self.current.line,
            column=self.current.column,
        )

    # ==========================================================
    # Program
    # ==========================================================

    def parse(self):

        statements = []

        while not self.is_end():

            statements.append(
                self.statement()
            )

        return Program(statements)


    # ==========================================================
# Multiplication / Division
# ==========================================================

def multiplication(self):

    node = self.primary()

    while self.current.type in (
        STAR,
        SLASH,
    ):

        operator = self.current.value

        self.advance()

        right = self.primary()

        node = Binary(
            node,
            operator,
            right,
        )

    return node


    # ==========================================================
# Addition / Subtraction
# ==========================================================

def addition(self):

    node = self.multiplication()

    while self.current.type in (
        PLUS,
        MINUS,
    ):

        operator = self.current.value

        self.advance()

        right = self.multiplication()

        node = Binary(
            node,
            operator,
            right,
        )

    return node 