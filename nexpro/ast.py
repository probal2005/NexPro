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
    pass


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