from nexpro.lexer import Lexer
from nexpro.parser import Parser

code = '''
name = "Probal"

say name
'''

lexer = Lexer(code)

tokens = lexer.tokenize()

parser = Parser(tokens)

print("=" * 50)
print("Current")
print("=" * 50)
print(parser.current)

print()

print("=" * 50)
print("Peek")
print("=" * 50)
print(parser.peek())

print()

parser.advance()

print("=" * 50)
print("After Advance")
print("=" * 50)
print(parser.current)

print()

print("=" * 50)
print("Previous")
print("=" * 50)
print(parser.previous())