from nexpro.lexer import Lexer
from nexpro.parser import Parser

code = open(
    "examples/parser1.pa"
).read()

lexer = Lexer(code)

tokens = lexer.tokenize()

parser = Parser(tokens)

tree = parser.parse()

print(tree)

print(type(tree).__name__)

print(tree.statements)