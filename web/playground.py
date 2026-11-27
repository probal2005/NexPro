"""Browser adapter for the NexPro interpreter and compiler."""

from contextlib import redirect_stdout
from io import StringIO
from json import dumps

from nexpro.compiler import compile_program
from nexpro.errors import NexProError
from nexpro.interpreter import Interpreter
from nexpro.lexer import Lexer
from nexpro.parser import Parser


def run_playground(source, action):
    output = StringIO()
    try:
        filename = "playground.pa"
        tree = Parser(Lexer(source, filename).tokenize(), filename).parse()
        if action == "compile":
            return dumps({"ok": True, "output": compile_program(tree)})
        with redirect_stdout(output):
            Interpreter().visit(tree)
    except NexProError as error:
        return dumps({"ok": False, "output": output.getvalue(), "error": str(error)})
    except (ArithmeticError, ValueError, TypeError, RecursionError) as error:
        return dumps({
            "ok": False,
            "output": output.getvalue(),
            "error": f"NexPro Runtime Error: {error}",
        })
    return dumps({"ok": True, "output": output.getvalue()})
