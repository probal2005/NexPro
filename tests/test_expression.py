from nexpro.lexer import Lexer
from nexpro.parser import Parser

code = open(
    "examples/math.pa"
).read()

lexer = Lexer(code)

tokens = lexer.tokenize()

print("=" * 50)
print("TOKENS")
print("=" * 50)

for token in tokens:
    print(token)

print()

parser = Parser(tokens)

print("Parser Ready ✓")