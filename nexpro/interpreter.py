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
    For,
    Break,
    Continue,
    Logical,
)

from nexpro.errors import EXECUTION_ERRORS
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


class _BreakLoop(Exception):
    pass


class _ContinueLoop(Exception):
    pass


class Interpreter:

    def __init__(self, read_input=input):
        self.globals = Runtime()
        self.runtime = self.globals
        self.functions = {}
        self.function_name = "<program>"
        self.builtins = {"len": len, "int": int, "float": float, "input": read_input, "append": list.append}

    # ---------------------------------

    def visit(self, node):
        try:
            return self._visit(node)
        except NexProRuntimeError as error:
            if not error.frames:
                error.add_frame(self.function_name, node.location)
            raise
        except EXECUTION_ERRORS as error:
            runtime_error = NexProRuntimeError(str(error))
            runtime_error.add_frame(self.function_name, node.location)
            raise runtime_error from error

    def _visit(self, node):

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
            try:
                while self.visit(node.condition):
                    try:
                        self.visit_block(node.body)
                    except _ContinueLoop:
                        continue
            except _BreakLoop:
                pass
            return None

        elif isinstance(node, For):
            try:
                for value in self.visit(node.iterable):
                    self.runtime.set(node.name, value)
                    try:
                        self.visit_block(node.body)
                    except _ContinueLoop:
                        continue
            except _BreakLoop:
                pass
            return None

        elif isinstance(node, Break):
            raise _BreakLoop

        elif isinstance(node, Continue):
            raise _ContinueLoop

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

        elif isinstance(node, Logical):
            left = bool(self.visit(node.left))
            if node.operator == "and":
                return left and bool(self.visit(node.right))
            return left or bool(self.visit(node.right))

        elif isinstance(node, Unary):
            value = self.visit(node.operand)
            if node.operator == "not":
                return not value
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
        caller_name = self.function_name
        self.runtime = Runtime()
        self.function_name = function.name
        try:
            for name, value in zip(function.parameters, arguments):
                self.runtime.set(name, value)
            self.visit_block(function.body)
        except _ReturnFromFunction as returned:
            return returned.value
        except NexProRuntimeError as error:
            error.add_frame(caller_name, node.location)
            raise
        finally:
            self.runtime = caller
            self.function_name = caller_name
        return None
