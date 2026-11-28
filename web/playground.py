"""Browser adapter for the NexPro interpreter and compiler."""

from contextlib import redirect_stdout
from io import StringIO
from json import dumps, loads

from nexpro.compiler import compile_program
from nexpro.data_builtins import _field_label, _number_field, _text_field
from nexpro.errors import NexProError
from nexpro.interpreter import Interpreter
from nexpro.loader import load_program


class PlaygroundOutput(StringIO):
    def write(self, text):
        if self.tell() + len(text) > 65536:
            raise NexProError("Playground output limit reached.")
        return super().write(text)


class ToolPreview:
    def __init__(self, values):
        self.values = values
        self.fields = {}
        self.results = []
        self.result_size = 0

    def field(self, label, default, kind, minimum=None):
        if label in self.fields:
            raise ValueError(f"Duplicate field label: {label}")
        if len(self.fields) >= 50:
            raise ValueError("A tool can have up to 50 fields.")
        value = self.values.get(label, default)
        if kind == "number":
            _number_field(label, value, minimum)
        else:
            _text_field(label, value)
        self.fields[label] = {"label": label, "kind": kind, "value": value, "minimum": minimum}
        return value

    def number_field(self, label, default, minimum=None):
        _number_field(label, default, minimum)
        return self.field(label, default, "number", minimum)

    def text_field(self, label, default=""):
        _text_field(label, default)
        return self.field(label, default, "text")

    def result(self, label, value):
        _field_label(label)
        text = str(value)
        self.result_size += len(label) + len(text)
        if len(self.results) >= 100 or self.result_size > 65536:
            raise ValueError("Tool result limit reached.")
        self.results.append({"label": label, "value": text})


def run_playground(source, action, input_text="", modules_json="{}", trace_enabled=False, fields_json="{}"):
    output = PlaygroundOutput()
    trace_lines = []
    preview = None

    def trace(line):
        if len(trace_lines) < 500:
            trace_lines.append(line)
        elif len(trace_lines) == 500:
            trace_lines.append("Trace limited to 500 statements.")

    def response(ok, error=None):
        result = {"ok": ok, "output": output.getvalue()}
        if error is not None:
            result["error"] = error
        if trace_enabled:
            result["trace"] = "\n".join(trace_lines)
        if preview is not None:
            result["tool"] = {"fields": list(preview.fields.values()), "results": preview.results if ok else []}
        return dumps(result)
    input_lines = StringIO(input_text, newline=None)

    def read_input(prompt=""):
        print(prompt, end="")
        line = input_lines.readline()
        if line == "":
            raise EOFError("EOF when reading a line")
        return line.removesuffix("\n")

    try:
        modules = loads(modules_json)

        def read_source(name):
            if name == "playground.pa":
                return source
            if name not in modules:
                raise FileNotFoundError("Add this .pa file under Module files")
            return modules[name]

        tree = load_program("playground.pa", read_source)
        if action == "check":
            return dumps({"ok": True, "output": "Syntax OK"})
        if action == "compile":
            return dumps({"ok": True, "output": compile_program(tree)})
        with redirect_stdout(output):
            interpreter = Interpreter(read_input=read_input, trace=trace if trace_enabled else None)
            if action == "preview":
                preview = ToolPreview(loads(fields_json))
                interpreter.builtins.update(
                    number_field=preview.number_field, text_field=preview.text_field, result=preview.result
                )
            interpreter.visit(tree)
    except NexProError as error:
        return response(False, str(error))
    except (ArithmeticError, ValueError, TypeError, RecursionError, IndexError, EOFError) as error:
        return response(False, f"NexPro Runtime Error: {error}")
    return response(True)
