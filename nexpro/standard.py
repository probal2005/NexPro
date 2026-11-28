"""Standard modules available to the interpreter and generated Python."""

import csv
import json
import math
import sys
from io import StringIO


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


def _csv_parse(text, required=None):
    if required is None:
        required = []
    if not isinstance(required, list) or any(not isinstance(name, str) or not name for name in required):
        raise TypeError("Required CSV columns must be a list of non-empty names.")
    if not isinstance(text, str):
        raise TypeError("CSV input must be text.")
    reader = csv.reader(StringIO(text.removeprefix("\ufeff"), newline=""), strict=True)
    try:
        headers = next((row for row in reader if row), None)
        if headers is None:
            if required:
                raise ValueError("CSV header is missing.")
            return []
        if not all(headers) or len(set(headers)) != len(headers):
            raise ValueError("CSV column names must be unique and non-empty.")
        missing = [name for name in required if name not in headers]
        if missing:
            raise ValueError("Missing CSV columns: " + ", ".join(missing))
        rows = []
        for row in reader:
            if not row:
                continue
            if len(row) != len(headers):
                raise ValueError(f"CSV row ending at line {reader.line_num} has the wrong number of columns.")
            rows.append(dict(zip(headers, row)))
        return rows
    except csv.Error as error:
        raise ValueError(f"Invalid CSV near line {reader.line_num}: {error}") from error


def _csv_stringify(rows):
    if not isinstance(rows, list):
        raise TypeError("CSV output requires a list of dictionaries.")
    if not rows:
        return ""
    if not isinstance(rows[0], dict) or not rows[0]:
        raise ValueError("CSV rows require named columns.")
    headers = list(rows[0])
    if any(not isinstance(name, str) or not name for name in headers):
        raise ValueError("CSV column names must be non-empty text.")
    output = StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(headers)
    for row in rows:
        if not isinstance(row, dict) or row.keys() != rows[0].keys():
            raise ValueError("All CSV rows must have the same columns.")
        values = [row[name] for name in headers]
        if any(value is not None and type(value) not in (str, bool, int, float) for value in values):
            raise ValueError("CSV cells must contain text, numbers, booleans, or null.")
        writer.writerow(values)
    return output.getvalue()


STANDARD_MODULES = {
    "std/math": {"abs": abs, "round": round, "sqrt": math.sqrt},
    "std/csv": {"parse": _csv_parse, "stringify": _csv_stringify},
    "std/json": {"parse": _json_parse, "stringify": _json_stringify},
}
