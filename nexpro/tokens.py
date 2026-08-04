"""
NexPro Programming Language
Token Definitions
Version 0.4.0
Author: Probal Dhali
"""

from dataclasses import dataclass


# ==========================================================
# Token Object
# ==========================================================

@dataclass(slots=True)
class Token:
    type: str
    value: object
    line: int
    column: int

    def __repr__(self):

        return (
            f"Token("
            f"type={self.type!r}, "
            f"value={self.value!r}, "
            f"line={self.line}, "
            f"column={self.column}"
            f")"
        )


# ==========================================================
# Special
# ==========================================================

EOF = "EOF"

NEWLINE = "NEWLINE"


# ==========================================================
# Literals
# ==========================================================

IDENTIFIER = "IDENTIFIER"

NUMBER = "NUMBER"

STRING = "STRING"

BOOLEAN = "BOOLEAN"


# ==========================================================
# Keywords
# ==========================================================

SAY = "SAY"

IF = "IF"

ELSE = "ELSE"

END = "END"

REPEAT = "REPEAT"

WHILE = "WHILE"

TRUE = "TRUE"

FALSE = "FALSE"


# ==========================================================
# Assignment
# ==========================================================

ASSIGN = "ASSIGN"


# ==========================================================
# Arithmetic
# ==========================================================

PLUS = "PLUS"

MINUS = "MINUS"

STAR = "STAR"

SLASH = "SLASH"

PERCENT = "PERCENT"


# ==========================================================
# Comparison
# ==========================================================

EQUAL = "EQUAL"

NOT_EQUAL = "NOT_EQUAL"

GREATER = "GREATER"

LESS = "LESS"

GREATER_EQUAL = "GREATER_EQUAL"

LESS_EQUAL = "LESS_EQUAL"


# ==========================================================
# Logical
# ==========================================================

AND = "AND"

OR = "OR"

NOT = "NOT"


# ==========================================================
# Symbols
# ==========================================================

LPAREN = "LPAREN"

RPAREN = "RPAREN"

LBRACKET = "LBRACKET"

RBRACKET = "RBRACKET"

LBRACE = "LBRACE"

RBRACE = "RBRACE"

COMMA = "COMMA"

COLON = "COLON"

DOT = "DOT"

NUMBER = "NUMBER"


# ==========================================================
# Reserved Keywords
# ==========================================================

KEYWORDS = {

    "say": SAY,

    "if": IF,

    "else": ELSE,

    "end": END,

    "repeat": REPEAT,

    "while": WHILE,

    "true": TRUE,

    "false": FALSE,

    "and": AND,

    "or": OR,

    "not": NOT,

}


# ==========================================================
# Single Character Tokens
# ==========================================================

SINGLE_CHAR_TOKENS = {

    "=": ASSIGN,

    "+": PLUS,

    "-": MINUS,

    "*": STAR,

    "/": SLASH,

    "%": PERCENT,

    "(": LPAREN,

    ")": RPAREN,

    "[": LBRACKET,

    "]": RBRACKET,

    "{": LBRACE,

    "}": RBRACE,

    ",": COMMA,

    ":": COLON,

    ".": DOT,

    ">": GREATER,

    "<": LESS,

}


# ==========================================================
# Double Character Tokens
# ==========================================================

DOUBLE_CHAR_TOKENS = {

    "==": EQUAL,

    "!=": NOT_EQUAL,

    ">=": GREATER_EQUAL,

    "<=": LESS_EQUAL,

}


# Operators
ASSIGN = "ASSIGN"

PLUS = "PLUS"
MINUS = "MINUS"
STAR = "STAR"
SLASH = "SLASH"
MODULO = "MODULO"

EQUAL = "EQUAL"
NOT_EQUAL = "NOT_EQUAL"

LESS = "LESS"
LESS_EQUAL = "LESS_EQUAL"

GREATER = "GREATER"
GREATER_EQUAL = "GREATER_EQUAL"

# Punctuation
LPAREN = "LPAREN"
RPAREN = "RPAREN"

LBRACE = "LBRACE"
RBRACE = "RBRACE"

LBRACKET = "LBRACKET"
RBRACKET = "RBRACKET"

COMMA = "COMMA"
DOT = "DOT"
COLON = "COLON"
SEMICOLON = "SEMICOLON"