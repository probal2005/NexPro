from nexpro.lexer import Lexer

code = """
a = 10 + 20

say a
"""

lexer = Lexer(code)

tokens = lexer.tokenize()

for token in tokens:
    print(token)