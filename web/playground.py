"""Browser adapter for the NexPro interpreter and compiler."""

from contextlib import redirect_stdout
from io import StringIO
from json import dumps

from nexpro.compiler import compile_program
from nexpro.errors import NexProError
from nexpro.interpreter import Interpreter
from nexpro.lexer import Lexer
from nexpro.parser import Parser


class PlaygroundOutput(StringIO):
    def write(self, text):
        if self.tell() + len(text) > 65536:
            raise NexProError("Playground output limit reached.")
        return super().write(text)


def run_playground(source, action, input_text=""):
    output = PlaygroundOutput()
    input_lines = StringIO(input_text, newline=None)

    def read_input(prompt=""):
        print(prompt, end="")
        line = input_lines.readline()
        if line == "":
            raise EOFError("EOF when reading a line")
        return line.removesuffix("\n")

    try:
        filename = "playground.pa"
        tree = Parser(Lexer(source, filename).tokenize(), filename).parse()
        if action == "compile":
            return dumps({"ok": True, "output": compile_program(tree)})
        with redirect_stdout(output):
            Interpreter(read_input=read_input).visit(tree)
    except NexProError as error:
        return dumps({"ok": False, "output": output.getvalue(), "error": str(error)})
    except (ArithmeticError, ValueError, TypeError, RecursionError, IndexError, EOFError) as error:
        return dumps({
            "ok": False,
            "output": output.getvalue(),
            "error": f"NexPro Runtime Error: {error}",
        })
    return dumps({"ok": True, "output": output.getvalue()})
