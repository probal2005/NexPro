"""Standard modules available to the interpreter and generated Python."""

import json
import math
import sys


def _configure_stdio():
    """Keep Unicode input and output available when redirected on Windows."""
    if sys.platform == "win32":
        for stream in (sys.stdin, sys.stdout, sys.stderr):
            if hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8")


def _json_parse(text):
    def reject_constant(value):
        raise ValueError(f"Invalid JSON constant: {value}")

    return json.loads(text, parse_constant=reject_constant)


def _json_stringify(value):
    return json.dumps(value, ensure_ascii=False, allow_nan=False)


STANDARD_MODULES = {
    "std/math": {"abs": abs, "round": round, "sqrt": math.sqrt},
    "std/json": {"parse": _json_parse, "stringify": _json_stringify},
}
