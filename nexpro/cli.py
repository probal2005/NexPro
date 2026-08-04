import sys

from nexpro.lexer import Lexer
from nexpro.parser import Parser
from nexpro.interpreter import Interpreter


def main():

    if len(sys.argv) != 3:

        print("Usage:")

        print("nexpro run file.pa")

        return

    command = sys.argv[1]

    filename = sys.argv[2]

    if command != "run":

        print("Unknown command")

        return

    with open(filename, "r") as file:

        code = file.read()

    lexer = Lexer(code)

    tokens = lexer.tokenize()

    parser = Parser(tokens)

    tree = parser.parse()

    interpreter = Interpreter()

    interpreter.visit(tree)


if __name__ == "__main__":

    main()