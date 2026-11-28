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


def _text_values(*values):
    if any(not isinstance(value, str) for value in values):
        raise TypeError("std/text requires strings.")
    return values


def _text_replace(text, old, new):
    text, old, new = _text_values(text, old, new)
    return text.replace(old, new)


def _text_find(text, fragment):
    text, fragment = _text_values(text, fragment)
    return text.find(fragment)


def _text_contains(text, fragment):
    text, fragment = _text_values(text, fragment)
    return fragment in text


def _text_starts_with(text, prefix):
    text, prefix = _text_values(text, prefix)
    return text.startswith(prefix)


def _text_ends_with(text, suffix):
    text, suffix = _text_values(text, suffix)
    return text.endswith(suffix)


def _as_list(items):
    if not isinstance(items, list):
        raise TypeError("std/list requires a list.")
    return items


def _list_insert(items, index, value):
    if type(index) is not int:
        raise TypeError("A list index must be an integer.")
    _as_list(items).insert(index, value)


def _list_pop(items, index=-1):
    if type(index) is not int:
        raise TypeError("A list index must be an integer.")
    return _as_list(items).pop(index)


def _list_remove(items, value):
    items = _as_list(items)
    try:
        items.remove(value)
    except ValueError:
        return False
    return True


def _list_unique(items):
    unique = []
    for value in _as_list(items):
        if value not in unique:
            unique.append(value)
    return unique


def _as_dict(record):
    if not isinstance(record, dict):
        raise TypeError("std/dict requires a dictionary.")
    return record


def _dict_has(record, key):
    return key in _as_dict(record)


def _dict_remove(record, key, default=None):
    return _as_dict(record).pop(key, default)


def _dict_merge(left, right):
    return {**_as_dict(left), **_as_dict(right)}


STANDARD_MODULES = {
    "std/text": {
        "replace": _text_replace, "find": _text_find, "contains": _text_contains,
        "starts_with": _text_starts_with, "ends_with": _text_ends_with,
    },
    "std/list": {"insert": _list_insert, "pop": _list_pop, "remove": _list_remove, "unique": _list_unique},
    "std/dict": {"has": _dict_has, "remove": _dict_remove, "merge": _dict_merge},
    "std/math": {"abs": abs, "round": round, "sqrt": math.sqrt},
    "std/csv": {"parse": _csv_parse, "stringify": _csv_stringify},
    "std/json": {"parse": _json_parse, "stringify": _json_stringify},
}
