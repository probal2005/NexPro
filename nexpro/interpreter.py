"""
NexPro Interpreter
Version 0.3.0
"""

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
)

from nexpro.errors import RuntimeError as NexProRuntimeError
from nexpro.runtime import Runtime


class Interpreter:

    def __init__(self):
        self.globals = Runtime()
        self.runtime = self.globals
        self.functions = {}

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

        for statement in node.statements:
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

        print(value)

    # ---------------------------------

    def visit_binary(self, node):

        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.operator == "+":
            return left + right

        elif node.operator == "-":
            return left - right

        elif node.operator == "*":
            return left * right

        elif node.operator == "/":
            return left / right

        raise Exception(
            f"Unknown operator {node.operator}"
        )

    def visit_call(self, node):
        arguments = [self.visit(argument) for argument in node.arguments]
        function = self.functions.get(node.name)
        if function is None:
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
            for statement in function.body:
                if isinstance(statement, Return):
                    return self.visit(statement.value)
                self.visit(statement)
        finally:
            self.runtime = caller
        return None
