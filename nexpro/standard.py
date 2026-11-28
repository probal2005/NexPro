"""Standard modules available to the interpreter and generated Python."""

import csv
import json
import math
import statistics
import sys
from collections import deque
from io import StringIO


class _CodedError(ValueError):
    def __init__(self, code, message, details=None):
        super().__init__(message)
        self.code = code
        self.details = details


def _error_code(error):
    if isinstance(error, _CodedError):
        return error.code
    for error_type, code in (
        (ZeroDivisionError, "division_by_zero"), (ArithmeticError, "arithmetic_error"),
        (TypeError, "invalid_type"), (KeyError, "missing_key"),
        (IndexError, "invalid_index"), (EOFError, "end_of_input"),
        (RecursionError, "recursion_limit"),
    ):
        if isinstance(error, error_type):
            return code
    return "runtime_error"


def _error_record(code, message, location, details=None):
    function, filename, line = location or (None, None, None)
    record = {"code": code, "message": message, "file": filename, "line": line, "function": function}
    if details is not None:
        record["details"] = details
    return record


_TYPE_NAMES = {
    type(None): "null", bool: "boolean", int: "integer", float: "float",
    str: "string", list: "list", dict: "dictionary",
}
RECORD_FIELD_TYPES = frozenset((*_TYPE_NAMES.values(), "queue", "linked_list", "record"))


def _type_of(value):
    kind = type(value)
    return _TYPE_NAMES.get(kind, getattr(kind, "_nexpro_type", kind.__name__))


class _Record(dict):
    _nexpro_type = "record"

    def __init__(self, name, fields, scope, field_types):
        self.name = name
        self.field_types = field_types
        for field in fields:
            self.validate(field, scope[field])
        super().__init__((field, scope[field]) for field in fields)

    def validate(self, field, value):
        expected = self.field_types.get(field)
        if expected is None:
            return
        actual = _type_of(value)
        if actual != expected:
            raise _CodedError(
                "record_field_type", f"Field '{field}' of record '{self.name}' expects {expected}, got {actual}",
                {"record": self.name, "field": field, "expected": expected, "actual": actual},
            )

    def __setitem__(self, key, value):
        if key not in self:
            raise KeyError(f"Record '{self.name}' has no field '{key}'")
        self.validate(key, value)
        super().__setitem__(key, value)

    def pop(self, key, default=None):
        if key in self:
            raise ValueError(f"Cannot remove field '{key}' from record '{self.name}'")
        return default


def _record_field(record, name):
    if not isinstance(record, _Record):
        raise TypeError("Dot access requires a record.")
    return record[name]


def _record_set_field(record, name, value):
    if not isinstance(record, _Record):
        raise TypeError("Dot assignment requires a record.")
    record[name] = value


def _record_from_dict(invoke, name, values):
    if not isinstance(name, str):
        raise TypeError("Record name must be text.")
    parts = name.split(".")
    if len(parts) not in (1, 2) or not all(part.isidentifier() for part in parts):
        raise ValueError("Expected a record name or module.record name.")
    if type(values) is not dict or any(not isinstance(key, str) for key in values):
        raise TypeError("Record input must be a dictionary with text keys.")
    return invoke(parts[0] if len(parts) == 2 else None, parts[-1], values)


def _record_to_dict(value):
    if not isinstance(value, _Record):
        raise TypeError("Expected a record.")
    return dict(value)


def _throw(message, code="thrown"):
    if not isinstance(code, str) or not code.strip() or not isinstance(message, str):
        raise TypeError("throw requires a text message and a non-empty text code.")
    raise _CodedError(code, message)


def _to_int(*args):
    try:
        return int(*args)
    except ValueError as error:
        raise _CodedError("invalid_integer", str(error)) from error


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
                raise _CodedError("csv_missing_columns", "CSV header is missing.")
            return []
        if not all(headers) or len(set(headers)) != len(headers):
            raise ValueError("CSV column names must be unique and non-empty.")
        missing = [name for name in required if name not in headers]
        if missing:
            raise _CodedError("csv_missing_columns", "Missing CSV columns: " + ", ".join(missing))
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


class _Queue:
    _nexpro_type = "queue"

    def __init__(self, items):
        self.items = deque(items)

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return "<queue>"


def _queue_new(items=None):
    return _Queue([] if items is None else _as_list(items))


def _queue_items(queue):
    if not isinstance(queue, _Queue):
        raise TypeError("std/queue requires a queue.")
    return queue.items


def _queue_enqueue(queue, value):
    _queue_items(queue).append(value)


def _queue_dequeue(queue):
    return _queue_items(queue).popleft()


def _queue_peek(queue):
    return _queue_items(queue)[0]


def _queue_to_list(queue):
    return list(_queue_items(queue))


class _Link:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node


class _LinkedList:
    _nexpro_type = "linked_list"

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self):
        return self.size

    def __repr__(self):
        return "<linked_list>"

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node.value
            node = node.next_node

    def append(self, value):
        node = _Link(value)
        if self.tail is None:
            self.head = node
        else:
            self.tail.next_node = node
        self.tail = node
        self.size += 1

    def node_at(self, index):
        node = self.head
        for _ in range(index):
            node = node.next_node
        return node


def _linked_new(items=None):
    linked = _LinkedList()
    if items is not None:
        for item in _as_list(items):
            linked.append(item)
    return linked


def _as_linked(linked):
    if not isinstance(linked, _LinkedList):
        raise TypeError("std/linked_list requires a linked list.")
    return linked


def _linked_index(index, stop):
    if type(index) is not int:
        raise TypeError("A linked-list index must be an integer.")
    if not 0 <= index < stop:
        raise IndexError("Linked-list index out of range.")


def _linked_append(linked, value):
    _as_linked(linked).append(value)


def _linked_insert(linked, index, value):
    linked = _as_linked(linked)
    _linked_index(index, linked.size + 1)
    if index == linked.size:
        linked.append(value)
        return
    if index == 0:
        linked.head = _Link(value, linked.head)
    else:
        previous = linked.node_at(index - 1)
        previous.next_node = _Link(value, previous.next_node)
    linked.size += 1


def _linked_remove(linked, index):
    linked = _as_linked(linked)
    _linked_index(index, linked.size)
    previous = None if index == 0 else linked.node_at(index - 1)
    if previous is None:
        removed = linked.head
        linked.head = removed.next_node
    else:
        removed = previous.next_node
        previous.next_node = removed.next_node
    if removed is linked.tail:
        linked.tail = previous
    linked.size -= 1
    return removed.value


def _linked_to_list(linked):
    return list(_as_linked(linked))


def _stats_numbers(items):
    items = _as_list(items)
    if not items or any(type(item) not in (int, float) or not -math.inf < item < math.inf for item in items):
        raise ValueError("Expected a non-empty list of finite numbers.")
    return items


def _stats_mean(items):
    return statistics.mean(_stats_numbers(items))


def _stats_median(items):
    return statistics.median(_stats_numbers(items))


def _stats_count_by(items, key=None):
    counts = {}
    for value in _as_list(items):
        group = value if key is None else _as_dict(value)[key]
        counts[group] = counts.get(group, 0) + 1
    return counts


STANDARD_MODULES = {
    "std/record": {"from_dict": _record_from_dict, "to_dict": _record_to_dict},
    "std/queue": {
        "new": _queue_new, "enqueue": _queue_enqueue, "dequeue": _queue_dequeue,
        "peek": _queue_peek, "to_list": _queue_to_list,
    },
    "std/linked_list": {
        "new": _linked_new, "append": _linked_append, "insert": _linked_insert,
        "remove": _linked_remove, "to_list": _linked_to_list,
    },
    "std/stats": {"mean": _stats_mean, "median": _stats_median, "count_by": _stats_count_by},
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
