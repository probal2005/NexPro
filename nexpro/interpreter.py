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
)

from nexpro.runtime import Runtime


class Interpreter:

    def __init__(self):
        self.runtime = Runtime()

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

        return self.runtime.get(node.name)

    # ---------------------------------

    def visit_string(self, node):

        return node.value

    # ---------------------------------

    def visit_number(self, node):

        return node.value

    # ---------------------------------

    def visit_say(self, node):

        value = self.visit(node.value)

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