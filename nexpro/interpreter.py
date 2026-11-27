"""
NexPro Interpreter
Version 0.3.0
"""

import operator

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
)

from nexpro.errors import RuntimeError as NexProRuntimeError
from nexpro.runtime import Runtime


BINARY_OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "==": operator.eq,
    "!=": operator.ne,
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
}


class _ReturnFromFunction(Exception):
    def __init__(self, value):
        self.value = value


class Interpreter:

    def __init__(self, read_input=input):
        self.globals = Runtime()
        self.runtime = self.globals
        self.functions = {}
        self.builtins = {"len": len, "int": int, "float": float, "input": read_input}

    # ---------------------------------

    def visit(self, node):

        if isinstance(node, Program):
            return self.visit_program(node)

        elif isinstance(node, Assign):
            return self.visit_assign(node)

        elif isinstance(node, Variable):
            return self.visit_variable(node)

        elif isinstance(node, String):
            return self.visit_string(node)

        elif isinstance(node, Number):
            return self.visit_number(node)

        elif isinstance(node, Boolean):
            return node.value

        elif isinstance(node, ListLiteral):
            return [self.visit(element) for element in node.elements]

        elif isinstance(node, Index):
            sequence = self.visit(node.sequence)
            index = self.visit(node.index)
            return sequence[index]

        elif isinstance(node, If):
            body = node.then_body if self.visit(node.condition) else node.else_body
            return self.visit_block(body or [])

        elif isinstance(node, While):
            while self.visit(node.condition):
                self.visit_block(node.body)
            return None

        elif isinstance(node, Return):
            raise _ReturnFromFunction(self.visit(node.value))

        elif isinstance(node, Say):
            return self.visit_say(node)

        elif isinstance(node, Binary):
            return self.visit_binary(node)

        elif isinstance(node, Function):
            self.functions[node.name] = node
            return None

        elif isinstance(node, Call):
            return self.visit_call(node)

        elif isinstance(node, Unary):
            value = self.visit(node.operand)
            return -value if node.operator == "-" else +value

        raise Exception(f"Unknown node: {type(node)}")

    # ---------------------------------

    def visit_program(self, node):

        self.visit_block(node.statements)

    def visit_block(self, statements):
        for statement in statements:
            self.visit(statement)

    # ---------------------------------

    def visit_assign(self, node):

        value = self.visit(node.value)

        self.runtime.set(
            node.variable.name,
            value
        )

    # ---------------------------------

    def visit_variable(self, node):

        if self.runtime.exists(node.name):
            return self.runtime.get(node.name)
        return self.globals.get(node.name)

    # ---------------------------------

    def visit_string(self, node):

        return node.value

    # ---------------------------------

    def visit_number(self, node):

        return node.value

    # ---------------------------------

    def visit_say(self, node):

        value = self.visit(node.expression)

        print(str(value).lower() if isinstance(value, bool) else value)

    # ---------------------------------

    def visit_binary(self, node):

        left = self.visit(node.left)
        right = self.visit(node.right)

        return BINARY_OPERATORS[node.operator](left, right)

    def visit_call(self, node):
        arguments = [self.visit(argument) for argument in node.arguments]
        function = self.functions.get(node.name)
        if function is None:
            if node.name in self.builtins:
                return self.builtins[node.name](*arguments)
            raise NexProRuntimeError(f"Undefined function '{node.name}'")
        expected = len(function.parameters)
        if len(arguments) != expected:
            raise NexProRuntimeError(
                f"Function '{node.name}' expects {expected} argument(s), got {len(arguments)}"
            )

        caller = self.runtime
        self.runtime = Runtime()
        try:
            for name, value in zip(function.parameters, arguments):
                self.runtime.set(name, value)
            self.visit_block(function.body)
        except _ReturnFromFunction as returned:
            return returned.value
        finally:
            self.runtime = caller
        return None
