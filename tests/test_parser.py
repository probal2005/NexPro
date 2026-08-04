from nexpro.lexer import Lexer
from nexpro.parser import Parser

with open("examples/variables.pa") as file:
    code = file.read()

lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)

print("Current:", parser.current)
print("Peek:", parser.peek())
print("End:", parser.is_end())