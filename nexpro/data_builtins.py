"""Data helpers used by the interpreter and standalone Python output."""


def _numeric_items(items, name):
    if not isinstance(items, list) or any(type(item) not in (int, float) for item in items):
        raise TypeError(f"{name}() expects a list of numbers")
    return items


def _sum_items(items):
    total = 0
    for item in _numeric_items(items, "sum"):
        total += item
    return total


def _min_items(items):
    if not _numeric_items(items, "min"):
        raise ValueError("min() requires at least one item")
    return min(items)


def _max_items(items):
    if not _numeric_items(items, "max"):
        raise ValueError("max() requires at least one item")
    return max(items)


def _record_keys(record):
    if not isinstance(record, dict):
        raise TypeError("keys() expects a dictionary")
    return list(record)


def _record_get(record, key, default):
    if not isinstance(record, dict):
        raise TypeError("get() expects a dictionary")
    return record.get(key, default)


DATA_BUILTINS = {
    "sum": _sum_items,
    "min": _min_items,
    "max": _max_items,
    "keys": _record_keys,
    "get": _record_get,
}
