"""
NexPro Programming Language
Abstract Syntax Tree (AST)
Version 0.4.0
Author: Probal Dhali
"""

from dataclasses import dataclass, field
from typing import List, Optional


# ==========================================================
# Base Node
# ==========================================================

class Node:
    """Base class for all AST nodes."""
    pass


# ==========================================================
# Program
# ==========================================================

@dataclass(slots=True)
class Program(Node):
    statements: List[Node] = field(default_factory=list)


# ==========================================================
# Literals
# ==========================================================

@dataclass(slots=True)
class Number(Node):
    value: int | float


@dataclass(slots=True)
class String(Node):
    value: str


@dataclass(slots=True)
class Boolean(Node):
    value: bool


# ==========================================================
# Variables
# ==========================================================

@dataclass(slots=True)
class Variable(Node):
    name: str


@dataclass(slots=True)
class Assign(Node):
    variable: Variable
    value: Node


# ==========================================================
# Statements
# ==========================================================

@dataclass(slots=True)
class Say(Node):
    value: Node


# ==========================================================
# Expressions
# ==========================================================

@dataclass(slots=True)
class Binary(Node):
    left: Node
    operator: str
    right: Node


@dataclass(slots=True)
class Unary(Node):
    operator: str
    operand: Node


# ==========================================================
# Control Flow
# ==========================================================

@dataclass(slots=True)
class If(Node):
    condition: Node
    body: List[Node]
    else_body: Optional[List[Node]] = None


@dataclass(slots=True)
class Repeat(Node):
    count: Node
    body: List[Node]


@dataclass(slots=True)
class While(Node):
    condition: Node
    body: List[Node]


# ==========================================================
# Future Features
# ==========================================================

@dataclass(slots=True)
class Function(Node):
    name: str
    parameters: List[str]
    body: List[Node]


@dataclass(slots=True)
class Return(Node):
    value: Node


@dataclass(slots=True)
class Call(Node):
    name: str
    arguments: List[Node]