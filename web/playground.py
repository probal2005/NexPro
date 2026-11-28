"""Browser adapter for the NexPro interpreter and compiler."""

from contextlib import redirect_stdout
from io import StringIO
from json import dumps, loads

from nexpro.compiler import compile_program
from nexpro.data_builtins import (
    _checkbox_field, _csv_field, _field_check, _field_label, _number_field, _select_field,
    _text_field, _validate_csv_download,
)
from nexpro.errors import NexProError
from nexpro.interpreter import Interpreter
from nexpro.loader import load_program
from nexpro.standard import _csv_parse


class PlaygroundOutput(StringIO):
    def write(self, text):
        if self.tell() + len(text) > 65536:
            raise NexProError("Playground output limit reached.")
        return super().write(text)


def _check_browser_number(value):
    if isinstance(value, (int, float)) and int(value) == value and abs(value) > (1 << 53) - 1:
        raise ValueError("Browser integer fields must be between -9007199254740991 and 9007199254740991.")


class ToolPreview:
    def __init__(self, values):
        self.values = values
        self.errors = {}
        self.downloads = {}
        self.download_size = 0
        self.fields = {}
        self.results = []
        self.result_size = 0

    def field(self, label, default, kind, **settings):
        if label in self.fields:
            raise ValueError(f"Duplicate field label: {label}")
        if len(self.fields) >= 50:
            raise ValueError("A tool can have up to 50 fields.")
        value = self.values.get(label, default)
        self.fields[label] = {"label": label, "kind": kind, "value": value, **settings}
        return value

    def number_field(self, label, default, minimum=None, maximum=None, step=None, message=None):
        _number_field(label, default, minimum, maximum, step, message)
        for number in (default, minimum, maximum, step):
            _check_browser_number(number)
        value = self.field(label, default, "number", minimum=minimum, maximum=maximum, step=step, message=message)
        checked = _number_field(label, value, minimum, maximum, step, message)
        _check_browser_number(checked)
        return checked

    def text_field(self, label, default=""):
        _text_field(label, default)
        return _text_field(label, self.field(label, default, "text"))

    def select_field(self, label, options, default=None):
        value = _select_field(label, options, default)
        value = self.field(label, value, "select", options=options)
        if value not in options:
            raise ValueError(f"{label} must be one of its options.")
        return value

    def checkbox_field(self, label, default=False):
        _checkbox_field(label, default)
        return _checkbox_field(label, self.field(label, default, "checkbox"))

    def field_check(self, label, condition, message):
        _field_check(label, True, message)
        if label not in self.fields:
            raise ValueError(f"Unknown field label: {label}")
        if not condition:
            self.errors.setdefault(label, message)
        return bool(condition)

    def csv_field(self, label, required=None, default=""):
        _csv_field(label, required, default)
        text = self.field(label, default, "file", required=True)
        self.fields[label].pop("value")
        if label not in self.values and not text:
            return ""
        try:
            _csv_field(label, required, text)
            if not text.strip():
                raise ValueError("The CSV file is empty.")
            _csv_parse(text, required)
        except (ValueError, TypeError) as error:
            self.errors[label] = str(error)
            return ""
        return text

    def download_csv(self, filename, text):
        _validate_csv_download(filename, text)
        size = len(text.encode("utf-8"))
        if filename in self.downloads:
            raise ValueError(f"Duplicate download filename: {filename}")
        if len(self.downloads) >= 10 or self.download_size + size > 512 * 1024:
            raise ValueError("Tool downloads exceeded the total output limit.")
        self.download_size += size
        self.downloads[filename] = text

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
            valid = ok and not preview.errors
            result["tool"] = {
                "fields": list(preview.fields.values()),
                "results": preview.results if valid else [],
                "errors": preview.errors,
                "downloads": preview.downloads if valid else {},
            }
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
                    number_field=preview.number_field, text_field=preview.text_field, result=preview.result,
                    select_field=preview.select_field, checkbox_field=preview.checkbox_field,
                    field_check=preview.field_check,
                    csv_field=preview.csv_field, download_csv=preview.download_csv,
                )
            interpreter.visit(tree)
    except NexProError as error:
        return response(False, str(error))
    except (ArithmeticError, ValueError, TypeError, RecursionError, IndexError, EOFError) as error:
        return response(False, f"NexPro Runtime Error: {error}")
    return response(True)
