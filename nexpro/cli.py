"""
NexPro CLI
Version 0.3.0
"""

import sys
from pathlib import Path

from nexpro import __version__
from nexpro.lexer import Lexer
from nexpro.parser import Parser
from nexpro.interpreter import Interpreter
from nexpro.errors import NexProError


def print_help():
    """Display NexPro CLI help."""

    print(f"""
=========================================
         NexPro Programming Language
               Version {__version__}
=========================================

Usage:

    nexpro <command> [file]

Commands:

    run <file.pa>     Run a NexPro program

    version           Show NexPro version

    help              Show this help message

Examples:

    nexpro run examples/hello.pa

    nexpro version

    nexpro help

=========================================
Official File Extension:

    .pa

Language:

    NexPro

=========================================
""")


def run_file(filename):
    """Run a NexPro source file."""

    path = Path(filename)

    if not path.exists():
        print(f"Error: File '{filename}' not found.")
        return

    if path.suffix != ".pa":
        print("Error: NexPro source files must end with '.pa'")
        return

    code = path.read_text(encoding="utf-8")

    lexer = Lexer(code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    tree = parser.parse()

    interpreter = Interpreter()
    interpreter.visit(tree)


def main():

    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1]

    if command == "help":
        print_help()
        return

    if command == "version":
        print(f"NexPro {__version__}")
        return

    if command == "run":

        if len(sys.argv) < 3:
            print("Error: Please specify a .pa file.")
            print("Example:")
            print("    nexpro run examples/hello.pa")
            return

        try:
            run_file(sys.argv[2])

        except NexProError as error:
            print(error)

        except Exception as error:
            print("Runtime Error")
            print(error)

        return

    print(f"Unknown command: {command}")
    print("Type 'nexpro help' for available commands.")


if __name__ == "__main__":
    main()