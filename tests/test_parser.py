from nexpro.lexer import Lexer
from nexpro.parser import Parser

code = """
name = "Probal"

say name
"""

lexer = Lexer(code)

tokens = lexer.tokenize()

parser = Parser(tokens)

tree = parser.parse()

print(tree)