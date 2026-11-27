"""Command-line tools for running and compiling NexPro programs."""

import argparse
import sys
from pathlib import Path

from nexpro import __version__
from nexpro.compiler import compile_program
from nexpro.errors import NexProError
from nexpro.interpreter import Interpreter
from nexpro.lexer import Lexer
from nexpro.parser import Parser


def load_program(path):
    if path.suffix != ".pa":
        raise NexProError("NexPro source files must end with '.pa'")
    source = path.read_text(encoding="utf-8")
    filename = str(path)
    return Parser(Lexer(source, filename).tokenize(), filename).parse()


def run_file(filename):
    Interpreter().visit(load_program(Path(filename)))


def main(argv=None):
    parser = argparse.ArgumentParser(prog="nexpro", description="NexPro language tools")
    parser.add_argument("--version", action="version", version=f"NexPro {__version__}")
    commands = parser.add_subparsers(dest="command")
    run = commands.add_parser("run", help="Run a NexPro program")
    run.add_argument("source", type=Path)
    compiler = commands.add_parser("compile", help="Compile a NexPro program to Python")
    compiler.add_argument("source", type=Path)
    compiler.add_argument("-o", "--output", type=Path, help="Output path (default: SOURCE.py)")
    commands.add_parser("version", help="Show the NexPro version")
    commands.add_parser("help", help="Show this help message")
    args = parser.parse_args(argv)

    if args.command in (None, "help"):
        parser.print_help()
        return 0
    if args.command == "version":
        print(f"NexPro {__version__}")
        return 0

    try:
        if args.command == "run":
            run_file(args.source)
        else:
            output = args.output or args.source.with_suffix(".py")
            if output.resolve() == args.source.resolve() or (
                output.exists() and args.source.exists() and output.samefile(args.source)
            ):
                raise NexProError("Output path must differ from the source path")
            python_source = compile_program(load_program(args.source))
            output.write_text(python_source, encoding="utf-8")
    except (NexProError, OSError, UnicodeError) as error:
        print(error, file=sys.stderr)
        return 1
    except (ArithmeticError, TypeError, ValueError) as error:
        print(f"NexPro Runtime Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
