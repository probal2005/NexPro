from nexpro.lexer import Lexer
from nexpro.parser import Parser
from nexpro.interpreter import Interpreter

code = '''
a = 10
b = 20

say a + b
'''

lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)

tree = parser.parse()

interpreter = Interpreter()

interpreter.visit(tree)

print("\nInterpreter Test Passed ✅")