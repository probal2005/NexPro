from nexpro.lexer import Lexer
from nexpro.parser import Parser

code = open(
    "examples/addition.pa"
).read()

lexer = Lexer(code)

tokens = lexer.tokenize()

parser = Parser(tokens)

tree = parser.parse()

print("=" * 60)
print("PROGRAM")
print("=" * 60)

print(tree)

print()

for node in tree.statements:

    print(type(node).__name__)