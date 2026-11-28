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
    FLOOR_DIVIDE,
    MODULO,
    POWER,
    LPAREN,
    RPAREN,
    LBRACKET,
    RBRACKET,
    LBRACE,
    RBRACE,
    COLON,
    DOT,
    COMMA,
    FUNCTION,
    RETURN,
    IMPORT,
    END,
    IF,
    ELSE,
    WHILE,
    TRUE,
    FALSE,
    EQUAL,
    NOT_EQUAL,
    AND,
    OR,
    NOT,
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
    Index,
    ListLiteral,
    Import,
    Member,
    Slice,
    Assert,
    For,
    Break,
    Continue,
    Logical,
    Dictionary,
    SetItem,
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

    def locate(self, node, token):
        node.location = (self.filename or "<input>", token.line)
        return node

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

            if self.match(DOT):
                member = self.expect(IDENTIFIER, "Expected member name")
                if self.match(LPAREN):
                    return self.locate(self.call(member.value, token.value), token)
                return self.locate(Member(token.value, member.value), token)
            if self.match(LPAREN):
                return self.locate(self.call(token.value), token)
            return self.locate(Variable(token.value), token)

        if self.match(LBRACE):
            entries = []
            if not self.check(RBRACE):
                while True:
                    key = self.expression()
                    self.expect(COLON, "Expected ':' after dictionary key")
                    entries.append((key, self.expression()))
                    if not self.match(COMMA):
                        break
            self.expect(RBRACE, "Expected '}' after dictionary entries")
            return self.locate(Dictionary(entries), token)

        if self.match(LBRACKET):
            elements = self.expression_list(RBRACKET)
            self.expect(RBRACKET, "Expected ']' after list elements")
            return self.locate(ListLiteral(elements), token)

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
        return self.logical_or()

    def logical_or(self):
        node = self.logical_and()
        while self.match(OR):
            operator = self.previous()
            node = self.locate(Logical(node, operator.value, self.logical_and()), operator)
        return node

    def logical_and(self):
        node = self.logical_not()
        while self.match(AND):
            operator = self.previous()
            node = self.locate(Logical(node, operator.value, self.logical_not()), operator)
        return node

    def logical_not(self):
        if self.match(NOT):
            token = self.previous()
            return self.locate(Unary(token.value, self.logical_not()), token)
        return self.comparison()

    def comparison(self):
        left = self.addition()
        if self.match(EQUAL, NOT_EQUAL, LESS, LESS_EQUAL, GREATER, GREATER_EQUAL):
            operator = self.previous()
            return self.locate(Binary(left, operator.value, self.addition()), operator)
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

    def expression_list(self, terminator):
        expressions = []
        if not self.check(terminator):
            expressions.append(self.expression())
            while self.match(COMMA):
                expressions.append(self.expression())
        return expressions

    def call(self, name, namespace=None):
        arguments = self.expression_list(RPAREN)
        self.expect(RPAREN, "Expected ')' after arguments")
        return Call(name, arguments, namespace)

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

    def block(self, *terminators, in_function, in_loop=False):
        body = []
        while not self.is_end() and self.current.type not in terminators:
            body.append(self.statement(in_function=in_function, in_loop=in_loop))
        return body

    def statement(self, in_function=False, top_level=False, in_loop=False):
        token = self.current
        node = self.parse_statement(in_function, top_level, in_loop)
        return self.locate(node, token)

    def parse_statement(self, in_function, top_level, in_loop):
        if top_level and self.match(FUNCTION):
            return self.function()

        if top_level and self.match(IMPORT):
            path = self.expect(STRING, "Expected a quoted module path")
            alias = None
            if self.check(IDENTIFIER) and self.current.value == "as" and self.current.line == path.line and self.peek().type != ASSIGN:
                self.advance()
                alias = self.expect(IDENTIFIER, "Expected module alias").value
            return Import(path.value, path.line, path.column, alias)

        if in_function and self.match(RETURN):
            return Return(self.expression())

        if self.match(IF):
            condition = self.expression()
            then_body = self.block(ELSE, END, in_function=in_function, in_loop=in_loop)
            else_body = None
            if self.match(ELSE):
                else_body = self.block(END, in_function=in_function, in_loop=in_loop)
            self.expect(END, "Expected 'end' after if block")
            return If(condition, then_body, else_body)

        if self.match(WHILE):
            condition = self.expression()
            body = self.block(END, in_function=in_function, in_loop=True)
            self.expect(END, "Expected 'end' after while block")
            return While(condition, body)

        if self.check(SAY):
            return self.say_statement()

        if self.check(IDENTIFIER):
            token = self.current
            following = self.peek()
            if token.value == "assert" and following is not None and following.type not in (
                ASSIGN, LPAREN, LBRACKET, DOT,
            ):
                self.advance()
                return Assert(self.expression())

            if token.value == "for" and following is not None and following.type == IDENTIFIER:
                self.advance()
                name = self.expect(IDENTIFIER, "Expected loop variable")
                if not self.check(IDENTIFIER) or self.current.value != "in":
                    raise ParserError(
                        "Expected 'in' after loop variable",
                        self.current.line, self.current.column, self.filename,
                    )
                self.advance()
                iterable = self.expression()
                body = self.block(END, in_function=in_function, in_loop=True)
                self.expect(END, "Expected 'end' after for block")
                return For(name.value, iterable, body)

            if token.value in ("break", "continue") and (following is None or following.type not in (ASSIGN, LPAREN, LBRACKET, DOT)):
                if not in_loop:
                    raise ParserError(
                        f"'{token.value}' can only be used inside a loop",
                        token.line, token.column, self.filename,
                    )
                self.advance()
                return Break() if token.value == "break" else Continue()

            if following is not None and following.type == LBRACKET:
                target = self.postfix()
                self.expect(ASSIGN, "Expected '=' after indexed target")
                return SetItem(target, self.expression())

            if following is not None and following.type == DOT:
                call = self.primary()
                if not isinstance(call, Call):
                    raise ParserError("Expected a module function call", token.line, token.column, self.filename)
                return call

            if following is not None and following.type == LPAREN:
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
            operator = self.previous()
            return self.locate(Unary(operator.value, self.unary()), operator)
        return self.power()

    def power(self):
        base = self.postfix()
        if self.match(POWER):
            operator = self.previous()
            return self.locate(Binary(base, operator.value, self.unary()), operator)
        return base

    def postfix(self):
        node = self.primary()
        while self.match(LBRACKET):
            bracket = self.previous()
            index = None if self.check(COLON) else self.expression()
            if self.match(COLON):
                stop = None if self.check(COLON) or self.check(RBRACKET) else self.expression()
                step = None
                if self.match(COLON) and not self.check(RBRACKET):
                    step = self.expression()
                index = self.locate(Slice(index, stop, step), bracket)
            self.expect(RBRACKET, "Expected ']' after index")
            node = self.locate(Index(node, index), bracket)
        return node

    def multiplication(self):
        node = self.unary()
        while self.match(STAR, SLASH, FLOOR_DIVIDE, MODULO):
            operator = self.previous()
            node = self.locate(Binary(node, operator.value, self.unary()), operator)
        return node


    def addition(self):
        node = self.multiplication()
        while self.match(PLUS, MINUS):
            operator = self.previous()
            node = self.locate(Binary(node, operator.value, self.multiplication()), operator)
        return node
