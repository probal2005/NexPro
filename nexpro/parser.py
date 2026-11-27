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
    LPAREN,
    RPAREN,
    COMMA,
    FUNCTION,
    RETURN,
    END,
    IF,
    ELSE,
    WHILE,
    TRUE,
    FALSE,
    EQUAL,
    NOT_EQUAL,
    LESS,
    LESS_EQUAL,
    GREATER,
    GREATER_EQUAL,
)

from nexpro.ast import (
    Program,
    Assign,
    Variable,
    String,
    Number,
    Say,
    Binary,
    Call,
    Function,
    Return,
    Unary,
    Boolean,
    If,
    While,
)

from nexpro.errors import ParserError


class Parser:

    def __init__(self, tokens, filename=None):

        self.filename = filename
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
            filename=self.filename,
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

        if self.match(TRUE, FALSE):
            return Boolean(token.type == TRUE)

        if token.type == IDENTIFIER:

            self.advance()

            if self.match(LPAREN):
                return self.call(token.value)
            return Variable(token.value)

        if self.match(LPAREN):
            node = self.expression()
            self.expect(RPAREN, "Expected ')'")
            return node

        raise ParserError(
            "Expected expression",
            line=token.line,
            column=token.column,
            filename=self.filename,
        )

    # ==========================================================
    # Expression
    # ==========================================================

    def expression(self):

        left = self.addition()
        if self.match(EQUAL, NOT_EQUAL, LESS, LESS_EQUAL, GREATER, GREATER_EQUAL):
            operator = self.previous().value
            return Binary(left, operator, self.addition())
        return left

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

    def call(self, name):
        arguments = []
        if not self.check(RPAREN):
            arguments.append(self.expression())
            while self.match(COMMA):
                arguments.append(self.expression())
        self.expect(RPAREN, "Expected ')' after arguments")
        return Call(name, arguments)

    def function(self):
        name = self.expect(IDENTIFIER, "Expected function name")
        self.expect(LPAREN, "Expected '(' after function name")
        parameters = []
        if not self.check(RPAREN):
            while True:
                parameter = self.expect(IDENTIFIER, "Expected parameter name")
                if parameter.value in parameters:
                    raise ParserError(
                        f"Duplicate parameter '{parameter.value}'",
                        parameter.line,
                        parameter.column,
                        self.filename,
                    )
                parameters.append(parameter.value)
                if not self.match(COMMA):
                    break
        self.expect(RPAREN, "Expected ')' after parameters")

        body = self.block(END, in_function=True)
        self.expect(END, "Expected 'end' after function body")
        return Function(name.value, parameters, body)

    def block(self, *terminators, in_function):
        body = []
        while not self.is_end() and self.current.type not in terminators:
            body.append(self.statement(in_function=in_function))
        return body

    def statement(self, in_function=False, top_level=False):
        if top_level and self.match(FUNCTION):
            return self.function()

        if in_function and self.match(RETURN):
            return Return(self.expression())

        if self.match(IF):
            condition = self.expression()
            then_body = self.block(ELSE, END, in_function=in_function)
            else_body = None
            if self.match(ELSE):
                else_body = self.block(END, in_function=in_function)
            self.expect(END, "Expected 'end' after if block")
            return If(condition, then_body, else_body)

        if self.match(WHILE):
            condition = self.expression()
            body = self.block(END, in_function=in_function)
            self.expect(END, "Expected 'end' after while block")
            return While(condition, body)

        if self.check(SAY):
            return self.say_statement()

        if self.check(IDENTIFIER):
            if self.peek() is not None and self.peek().type == LPAREN:
                name = self.current.value
                self.advance()
                self.advance()
                return self.call(name)
            return self.assignment()

        raise ParserError(
            "Unknown statement",
            line=self.current.line,
            column=self.current.column,
            filename=self.filename,
        )

    # ==========================================================
    # Program
    # ==========================================================

    def parse(self):

        statements = []

        while not self.is_end():

            statements.append(
                self.statement(top_level=True)
            )

        return Program(statements)



    def unary(self):
        if self.match(PLUS, MINUS):
            return Unary(self.previous().value, self.unary())
        return self.primary()

    def multiplication(self):
        node = self.unary()
        while self.match(STAR, SLASH):
            operator = self.previous().value
            node = Binary(node, operator, self.unary())
        return node


    def addition(self):
        node = self.multiplication()
        while self.match(PLUS, MINUS):
            operator = self.previous().value
            node = Binary(node, operator, self.multiplication())
        return node
