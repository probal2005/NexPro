"""
NexPro Interpreter
Version 0.3.0
"""

import operator

from nexpro.ast import (
    Program,
    Module,
    Member,
    Slice,
    Assert,
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
    Dictionary,
    SetItem,
)

from nexpro.data_builtins import DATA_BUILTINS
from nexpro.errors import EXECUTION_ERRORS
from nexpro.errors import RuntimeError as NexProRuntimeError
from nexpro.runtime import Runtime
from nexpro.standard import STANDARD_MODULES


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

    def __init__(self, read_input=input, trace=None, observer=None):
        self.globals = Runtime()
        self.runtime = self.globals
        self.trace = trace
        self.observer = observer
        self.function_depth = 0
        self.aliases = {}
        self.modules = {}
        self.module_bodies = {}
        self.functions = {}
        self.function_name = "<program>"
        self.builtins = {
            **DATA_BUILTINS,
            "len": len,
            "int": int,
            "float": float,
            "input": read_input,
            "append": list.append,
        }

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

        elif isinstance(node, Module):
            if node.path not in self.modules:
                module = Interpreter(read_input=self.builtins["input"], trace=self.trace, observer=self.observer)
                module.modules = self.modules
                module.module_bodies = self.module_bodies
                module.function_depth = self.function_depth
                if node.path in STANDARD_MODULES:
                    module.functions.update(STANDARD_MODULES[node.path])
                else:
                    module.visit_block(self.module_bodies[node.path])
                self.modules[node.path] = module
            self.aliases[node.alias] = self.modules[node.path]
            return None

        elif isinstance(node, Member):
            return self.get_module(node.namespace).globals.get(node.name)

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

        elif isinstance(node, Dictionary):
            return {self.visit(key): self.visit(value) for key, value in node.entries}

        elif isinstance(node, SetItem):
            sequence = self.visit(node.target.sequence)
            index = self.visit(node.target.index)
            value = self.visit(node.value)
            sequence[index] = value
            return None

        elif isinstance(node, Slice):
            return slice(*(self.visit(item) if item is not None else None
                           for item in (node.start, node.stop, node.step)))

        elif isinstance(node, Index):
            sequence = self.visit(node.sequence)
            index = self.visit(node.index)
            return sequence[index]

        elif isinstance(node, Assert):
            if not self.visit(node.condition):
                raise NexProRuntimeError("Assertion failed")
            return None

        elif isinstance(node, If):
            body = node.then_body if self.visit(node.condition) else node.else_body
            return self.visit_block(body or [])

        elif isinstance(node, While):
            try:
                while self.visit(node.condition):
                    if self.observer is not None and not node.body:
                        self.observer(self, node)
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

        self.module_bodies = getattr(node, 'modules', {})
        self.visit_block(node.statements)

    def visit_block(self, statements):
        for statement in statements:
            if self.observer is not None:
                self.observer(self, statement)
            if self.trace is not None and statement.location is not None:
                filename, line = statement.location
                self.trace(f"[trace] {filename}:{line} in {self.function_name}")
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

    def get_module(self, namespace):
        if namespace not in self.aliases:
            raise NexProRuntimeError(f"Undefined module alias '{namespace}'")
        return self.aliases[namespace]

    def visit_call(self, node):
        arguments = [self.visit(argument) for argument in node.arguments]
        if node.namespace is not None:
            module = self.get_module(node.namespace)
            previous_depth = module.function_depth
            module.function_depth = self.function_depth
            try:
                return module.call_function(node.name, arguments, node, allow_builtin=False)
            except NexProRuntimeError as error:
                if error.frames:
                    error.add_frame(self.function_name, node.location)
                raise
            finally:
                module.function_depth = previous_depth
        return self.call_function(node.name, arguments, node)

    def call_function(self, name, arguments, node, allow_builtin=True):
        function = self.functions.get(name)
        if function is None:
            if allow_builtin and name in self.builtins:
                return self.builtins[name](*arguments)
            raise NexProRuntimeError(f"Undefined function '{node.name}'")
        if callable(function):
            return function(*arguments)
        expected = len(function.parameters)
        if len(arguments) != expected:
            raise NexProRuntimeError(
                f"Function '{node.name}' expects {expected} argument(s), got {len(arguments)}"
            )

        caller = self.runtime
        caller_name = self.function_name
        self.runtime = Runtime()
        self.function_name = function.name
        self.function_depth += 1
        try:
            for name, value in zip(function.parameters, arguments):
                self.runtime.set(name, value)
            self.visit_block(function.body)
        except _ReturnFromFunction as returned:
            return returned.value
        except NexProRuntimeError as error:
            if allow_builtin:
                error.add_frame(caller_name, node.location)
            raise
        finally:
            self.runtime = caller
            self.function_name = caller_name
            self.function_depth -= 1
        return None
