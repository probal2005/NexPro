"""Data helpers used by the interpreter and standalone Python output."""

import re
from fractions import Fraction


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


def _field_label(label):
    if not isinstance(label, str) or not label.strip() or len(label) > 120:
        raise ValueError("A field or result label must contain 1 to 120 characters.")


def _number_field(label, default, minimum=None, maximum=None, step=None, message=None):
    _field_label(label)
    for value in [default, *(bound for bound in (minimum, maximum, step) if bound is not None)]:
        if type(value) not in (int, float) or not -float("inf") < value < float("inf"):
            raise ValueError("Number fields require finite numbers.")
    if message is not None and not isinstance(message, str):
        raise TypeError("A field message must be text.")
    if minimum is not None and maximum is not None and minimum > maximum:
        raise ValueError("Field minimum cannot exceed its maximum.")
    if step is not None and step <= 0:
        raise ValueError("A number field step must be positive.")
    if minimum is not None and default < minimum:
        raise ValueError(message or f"{label} must be at least {minimum}.")
    if maximum is not None and default > maximum:
        raise ValueError(message or f"{label} must be at most {maximum}.")
    if step is not None:
        value, base, increment = map(lambda number: Fraction(str(number)), (default, minimum or 0, step))
        if ((value - base) / increment).denominator != 1:
            raise ValueError(message or f"{label} must follow the step of {step}.")
    return default


def _select_field(label, options, default=None):
    _field_label(label)
    if (not isinstance(options, list) or not 1 <= len(options) <= 100
            or any(not isinstance(option, str) or not 1 <= len(option) <= 120 for option in options)
            or len(set(options)) != len(options)):
        raise ValueError("Select fields need 1 to 100 unique text options.")
    value = options[0] if default is None else default
    if value not in options:
        raise ValueError(f"{label} must be one of its options.")
    return value


def _checkbox_field(label, default=False):
    _field_label(label)
    if type(default) is not bool:
        raise TypeError("Checkbox fields require a boolean.")
    return default


def _field_check(label, condition, message):
    _field_label(label)
    if not isinstance(message, str) or not 1 <= len(message) <= 500:
        raise ValueError("A validation message must contain 1 to 500 characters.")
    if not condition:
        raise ValueError(f"{label}: {message}")
    return True


def _text_field(label, default=""):
    _field_label(label)
    if not isinstance(default, str) or len(default) > 4096:
        raise ValueError("Text fields accept up to 4096 characters.")
    return default


def _result(label, value):
    _field_label(label)
    print(f"{label}: {value}")


DATA_BUILTINS.update({"number_field": _number_field, "text_field": _text_field, "result": _result})

DATA_BUILTINS.update({"select_field": _select_field, "checkbox_field": _checkbox_field, "field_check": _field_check})


def _csv_field(label, required=None, default=""):
    _field_label(label)
    if required is not None and (not isinstance(required, list) or len(required) > 100
            or any(not isinstance(name, str) or not 1 <= len(name) <= 120 for name in required)):
        raise ValueError("CSV fields need a list of up to 100 column names.")
    if not isinstance(default, str) or len(default.encode("utf-8")) > 512 * 1024:
        raise ValueError("CSV fields accept up to 512 KB of UTF-8 text.")
    return default


def _validate_csv_download(filename, text):
    if not isinstance(filename, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,115}\.csv", filename):
        raise ValueError("Use a simple filename ending in .csv.")
    if not isinstance(text, str) or len(text.encode("utf-8")) > 512 * 1024:
        raise ValueError("CSV downloads accept up to 512 KB of UTF-8 text.")


def _download_csv(filename, text):
    _validate_csv_download(filename, text)
    print(text, end="")


DATA_BUILTINS.update({"csv_field": _csv_field, "download_csv": _download_csv})


def _extended_arithmetic(symbol, left, right):
    if type(left) not in (int, float) or type(right) not in (int, float):
        raise TypeError(f"{symbol} requires numeric operands.")
    if symbol == "//":
        return left // right
    if symbol == "%":
        return left % right

    if type(left) is int and type(right) is int and abs(left) > 1:
        if right > 1_000_000 // abs(left).bit_length():
            raise ValueError("Integer power exceeds the 1,000,000-bit computation limit.")
    result = left ** right
    if isinstance(result, complex):
        raise ValueError("Power must produce a real number.")
    return result


def _argument_scope(name, parameters, default_count, arguments, named):
    maximum = len(parameters)
    minimum = maximum - default_count
    if len(arguments) > maximum or (not named and len(arguments) < minimum):
        expected = str(maximum) if minimum == maximum else f"{minimum} to {maximum}"
        raise ValueError(f"Function '{name}' expects {expected} argument(s), got {len(arguments)}")
    scope = dict(zip(parameters, arguments))
    for argument, value in named.items():
        if argument not in parameters:
            raise ValueError(f"Function '{name}' has no parameter '{argument}'")
        if argument in scope:
            raise ValueError(f"Function '{name}' got multiple values for '{argument}'")
        scope[argument] = value
    for parameter in parameters[:minimum]:
        if parameter not in scope:
            raise ValueError(f"Function '{name}' is missing required argument '{parameter}'")
    return scope


def _call_builtin(name, function, arguments, named):
    if named:
        raise ValueError(f"Built-in function '{name}' accepts only positional arguments")
    return function(*arguments)


def _say_value(value):
    if value is None:
        print("null")
    else:
        print(str(value).lower() if isinstance(value, bool) else value)


def _type_of(value):
    return {
        type(None): "null", bool: "boolean", int: "integer", float: "float",
        str: "string", list: "list", dict: "dictionary",
    }.get(type(value), getattr(type(value), "_nexpro_type", type(value).__name__))


DATA_BUILTINS["type_of"] = _type_of
