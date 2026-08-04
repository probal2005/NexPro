from nexpro.lexer import Lexer

code = '''
name = "Probal"
say name
'''

lexer = Lexer(code)
tokens = lexer.tokenize()

print("=== TOKENS ===")

for token in tokens:
    print(token)

print("\nLexer Test Passed ✅")