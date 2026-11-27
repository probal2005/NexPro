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
from nexpro.project import find_project, init_project


def load_program(path, output=None, project_root=None):
    if path.suffix != ".pa":
        raise NexProError("NexPro source files must end with '.pa'")
    root = project_root or path.parent.resolve()
    entry = path.resolve().relative_to(root).as_posix()
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

    def filename_for(name):
        if project_root is not None:
            return str(root / name)
        return str(path.parent / name)

    return load_modules(entry, read_source, filename_for=filename_for)


def run_file(filename, trace=None, project_root=None):
    Interpreter(trace=trace).visit(load_program(Path(filename), project_root=project_root))


def check_json(path, project_root=None):
    try:
        load_program(path, project_root=project_root)
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


def test_project():
    project = find_project()
    if project is None:
        raise NexProError("Run nexpro test inside a NexPro project")
    files = sorted(project.tests.rglob("test_*.pa"))
    if not files:
        raise NexProError(f"No test_*.pa files found in {project.tests}")
    failures = 0
    for path in files:
        try:
            run_file(path, project_root=project.root)
        except (NexProError, OSError, UnicodeError, ValueError, RecursionError) as error:
            failures += 1
            print(f"FAIL {path.relative_to(project.root)}\n{error}", file=sys.stderr)
        else:
            print(f"PASS {path.relative_to(project.root)}")
    print(f"{len(files) - failures} passed, {failures} failed")
    return int(failures > 0)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="nexpro", description="NexPro language tools")
    parser.add_argument("--version", action="version", version=f"NexPro {__version__}")
    commands = parser.add_subparsers(dest="command")
    run = commands.add_parser("run", help="Run a NexPro program")
    run.add_argument("source", type=Path, nargs="?")
    run.add_argument("--trace", action="store_true", help="Print executed NexPro statements to stderr")
    check = commands.add_parser("check", help="Check syntax and imports without running")
    check.add_argument("source", type=Path, nargs="?")
    check.add_argument("--json", action="store_true", help="Print machine-readable diagnostics")
    compiler = commands.add_parser("compile", help="Compile a NexPro program to Python")
    compiler.add_argument("source", type=Path, nargs="?")
    compiler.add_argument("-o", "--output", type=Path, help="Output path (default: SOURCE.py)")
    initialize = commands.add_parser("init", help="Create a NexPro project")
    initialize.add_argument("directory", type=Path, nargs="?", default=Path("."))
    commands.add_parser("test", help="Run a project's NexPro tests")
    commands.add_parser("version", help="Show the NexPro version")
    commands.add_parser("debug-adapter", help="Start the VS Code debug adapter")
    commands.add_parser("help", help="Show this help message")
    args = parser.parse_args(argv)

    if args.command in (None, "help"):
        parser.print_help()
        return 0
    if args.command == "version":
        print(f"NexPro {__version__}")
        return 0

    if args.command == "debug-adapter":
        from nexpro.debug_adapter import serve_debug_adapter
        serve_debug_adapter(load_program)
        return 0

    try:
        if args.command == "init":
            init_project(args.directory)
            print(f"Initialized NexPro project in {args.directory}")
            return 0
        if args.command == "test":
            return test_project()
        project = find_project() if args.source is None else None
        if args.source is None:
            if project is None:
                raise NexProError("Provide a .pa file or run inside a NexPro project")
            args.source = project.entry
        root = project.root if project else None
        if args.command == "run":
            trace = (lambda line: print(line, file=sys.stderr)) if args.trace else None
            run_file(args.source, trace=trace, project_root=root)
        elif args.command == "check":
            if args.json:
                return check_json(args.source, project_root=root)
            load_program(args.source, project_root=root)
            print("Syntax OK")
        else:
            output = args.output or args.source.with_suffix(".py")
            python_source = compile_program(load_program(args.source, output=output, project_root=root))
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
