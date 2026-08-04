"""
NexPro AST
Version 0.3.0
"""

from dataclasses import dataclass


# ==========================
# Base Node
# ==========================

class Node:
    pass


# ==========================
# Program
# ==========================

@dataclass
class Program(Node):

    statements: list


# ==========================
# Variable
# ==========================

@dataclass
class Variable(Node):

    name: str


# ==========================
# Number
# ==========================

@dataclass
class Number(Node):

    value: int


# ==========================
# String
# ==========================

@dataclass
class String(Node):

    value: str


# ==========================
# Assignment
# ==========================

@dataclass
class Assign(Node):

    variable: Variable

    value: Node


# ==========================
# Say
# ==========================

@dataclass
class Say(Node):

    value: Node


# ==========================
# Binary Expression
# ==========================

@dataclass
class Binary(Node):

    left: Node

    operator: str

    right: Node

@dataclass
class Unary(Node):

    operator: str

    operand: Node