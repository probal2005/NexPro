"""
NexPro Programming Language
Abstract Syntax Tree (AST)
Version 0.5.0
Author: Probal Dhali
"""


# ==========================================================
# Base Node
# ==========================================================

class Node:
    """Base class for every AST node."""
    location = None


# ==========================================================
# Program
# ==========================================================

class Program(Node):

    def __init__(self, statements):
        self.statements = statements


# ==========================================================
# Statement Base
# ==========================================================

class Statement(Node):
    pass


# ==========================================================
# Expression Base
# ==========================================================

class Expression(Node):
    pass


# ==========================================================
# Assignment
# ==========================================================

class Assign(Statement):

    def __init__(self, variable, value):
        self.variable = variable
        self.value = value


# ==========================================================
# Say Statement
# ==========================================================

class Say(Statement):

    def __init__(self, expression):
        self.expression = expression


# ==========================================================
# Variable
# ==========================================================

class Variable(Expression):

    def __init__(self, name):
        self.name = name


# ==========================================================
# Number
# ==========================================================

class Number(Expression):

    def __init__(self, value):
        self.value = value


# ==========================================================
# String
# ==========================================================

class String(Expression):

    def __init__(self, value):
        self.value = value


# ==========================================================
# Binary Expression
# ==========================================================

class Binary(Expression):

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Function(Statement):
    def __init__(self, name, parameters, body, defaults=()):
        self.name = name
        self.parameters = parameters
        self.defaults = defaults
        self.body = body


class Call(Expression, Statement):
    def __init__(self, name, arguments, namespace=None):
        self.name = name
        self.arguments = arguments
        self.namespace = namespace


class Return(Statement):
    def __init__(self, value):
        self.value = value


class Unary(Expression):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand


class Boolean(Expression):
    def __init__(self, value):
        self.value = value


class Null(Expression):
    pass


class If(Statement):
    def __init__(self, condition, then_body, else_body):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body


class While(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class ListLiteral(Expression):
    def __init__(self, elements):
        self.elements = elements


class Index(Expression):
    def __init__(self, sequence, index):
        self.sequence = sequence
        self.index = index


class Import(Statement):
    def __init__(self, path, line, column, alias=None):
        self.alias = alias
        self.path = path
        self.line = line
        self.column = column


class For(Statement):
    def __init__(self, name, iterable, body):
        self.name = name
        self.iterable = iterable
        self.body = body


class Break(Statement):
    pass


class Logical(Expression):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Continue(Statement):
    pass


class Dictionary(Expression):
    def __init__(self, entries):
        self.entries = entries


class SetItem(Statement):
    def __init__(self, target, value):
        self.target = target
        self.value = value


class Member(Expression):
    def __init__(self, namespace, name):
        self.namespace = namespace
        self.name = name


class Module(Statement):
    def __init__(self, alias, path):
        self.alias = alias
        self.path = path


class Slice(Expression):
    def __init__(self, start, stop, step):
        self.start = start
        self.stop = stop
        self.step = step


class Try(Statement):
    def __init__(self, body, error_name, handler, structured=False):
        self.body = body
        self.error_name = error_name
        self.handler = handler
        self.structured = structured


class Throw(Statement):
    def __init__(self, message, code=None):
        self.message = message
        self.code = code


class Assert(Statement):
    def __init__(self, condition):
        self.condition = condition
