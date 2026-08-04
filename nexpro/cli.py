import argparse

from nexpro.lexer import tokenize
from nexpro.parser import parse
from nexpro.interpreter import execute


def main():

    parser = argparse.ArgumentParser(
        prog="nexpro"
    )

    sub = parser.add_subparsers(dest="command")

    run_parser = sub.add_parser("run")

    run_parser.add_argument("file")

    args = parser.parse_args()

    if args.command == "run":

        with open(args.file, "r", encoding="utf-8") as f:

            code = f.read()

        tokens = tokenize(code)

        ast = parse(tokens)

        execute(ast)

    else:

        parser.print_help()
