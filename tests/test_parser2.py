from nexpro.lexer import Lexer
from nexpro.parser import Parser

code = open(
    "examples/parser2.pa"
).read()

lexer = Lexer(code)

tokens = lexer.tokenize()

parser = Parser(tokens)

tree = parser.parse()

print("=" * 50)
print("AST")
print("=" * 50)

print(tree)

print()

print(tree.statements)

print()

for node in tree.statements:

    print(type(node).__name__)