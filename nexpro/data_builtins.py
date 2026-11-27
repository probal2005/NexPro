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


def _require_text(value, name):
    if not isinstance(value, str):
        raise TypeError(f"{name}() expects text")


def _trim_text(text):
    _require_text(text, "trim")
    return text.strip()


def _lower_text(text):
    _require_text(text, "lower")
    return text.lower()


def _upper_text(text):
    _require_text(text, "upper")
    return text.upper()


def _split_text(text, separator):
    _require_text(text, "split")
    if not isinstance(separator, str):
        raise TypeError("split() expects a text separator")
    if not separator:
        raise ValueError("split() requires a non-empty separator")
    return text.split(separator)


def _join_text(items, separator):
    if not isinstance(items, list) or any(not isinstance(item, str) for item in items):
        raise TypeError("join() expects a list of text values")
    if not isinstance(separator, str):
        raise TypeError("join() expects a text separator")
    return separator.join(items)


DATA_BUILTINS.update({
    "trim": _trim_text,
    "lower": _lower_text,
    "upper": _upper_text,
    "split": _split_text,
    "join": _join_text,
})


def _range_items(start, stop=None, step=1):
    if stop is None:
        start, stop = 0, start
    if any(type(value) is not int for value in (start, stop, step)):
        raise TypeError("range() expects integer bounds and step")
    return list(range(start, stop, step))


def _sorted_items(items):
    if not isinstance(items, list):
        raise TypeError("sorted() expects a list")
    return sorted(items)


def _reverse_items(items):
    if not isinstance(items, list):
        raise TypeError("reverse() expects a list")
    return items[::-1]


DATA_BUILTINS.update({"range": _range_items, "sorted": _sorted_items, "reverse": _reverse_items})
