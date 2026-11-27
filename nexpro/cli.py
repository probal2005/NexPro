"""Command-line tools for running and compiling NexPro programs."""

import argparse
import json
import sys
from pathlib import Path

from nexpro import __version__
from nexpro.compiler import compile_program
from nexpro.errors import NexProError, SourceError
from nexpro.interpreter import Interpreter
from nexpro.loader import load_program as load_modules


def load_program(path, output=None):
    if path.suffix != ".pa":
        raise NexProError("NexPro source files must end with '.pa'")
    root = path.parent.resolve()
    destination = output.resolve() if output is not None else None

    def read_source(name):
        source = root / name
        resolved = source.resolve()
        if not resolved.is_relative_to(root):
            raise OSError("Module must stay inside the entry file's directory")
        if destination is not None and (
            resolved == destination or (
                output.exists() and source.exists() and output.samefile(source)
            )
        ):
            raise OSError("Output path must differ from every source path")
        return source.read_text(encoding="utf-8")

    return load_modules(path.name, read_source, filename_for=lambda name: str(path.parent / name))


def run_file(filename):
    Interpreter().visit(load_program(Path(filename)))


def check_json(path):
    try:
        load_program(path)
    except (NexProError, OSError, UnicodeError, ValueError, RecursionError) as error:
        diagnostic = {"message": str(error)}
        if isinstance(error, SourceError):
            diagnostic = {
                "message": error.message,
                "filename": error.filename,
                "line": error.line,
                "column": error.column,
            }
        print(json.dumps({"ok": False, "diagnostics": [diagnostic]}))
        return 1
    print(json.dumps({"ok": True, "diagnostics": []}))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(prog="nexpro", description="NexPro language tools")
    parser.add_argument("--version", action="version", version=f"NexPro {__version__}")
    commands = parser.add_subparsers(dest="command")
    run = commands.add_parser("run", help="Run a NexPro program")
    run.add_argument("source", type=Path)
    check = commands.add_parser("check", help="Check syntax and imports without running")
    check.add_argument("source", type=Path)
    check.add_argument("--json", action="store_true", help="Print machine-readable diagnostics")
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
        elif args.command == "check":
            if args.json:
                return check_json(args.source)
            load_program(args.source)
            print("Syntax OK")
        else:
            output = args.output or args.source.with_suffix(".py")
            python_source = compile_program(load_program(args.source, output=output))
            output.write_text(python_source, encoding="utf-8")
    except (NexProError, OSError, UnicodeError) as error:
        print(error, file=sys.stderr)
        return 1
    except (ArithmeticError, TypeError, ValueError, RecursionError, IndexError, EOFError) as error:
        print(f"NexPro Runtime Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
