"""
NexPro Token Definitions
Version 0.3.0
"""

from dataclasses import dataclass


# ==========================
# Token Types
# ==========================

SAY = "SAY"

IDENTIFIER = "IDENTIFIER"

STRING = "STRING"

NUMBER = "NUMBER"

ASSIGN = "ASSIGN"

PLUS = "PLUS"

MINUS = "MINUS"

STAR = "STAR"

SLASH = "SLASH"

LPAREN = "LPAREN"

RPAREN = "RPAREN"

EOF = "EOF"


# ==========================
# Token Class
# ==========================

@dataclass
class Token:

    type: str

    value: object

    line: int

    column: int

    def __repr__(self):

        return (
            f"Token("
            f"{self.type}, "
            f"{self.value}, "
            f"{self.line}:{self.column}"
            f")"
        )