# NexPro language reference

This reference and the [grammar](grammar.md) describe the supported language. The CLI interpreter and compiler use the same parser. A program is
UTF-8 text, typically saved with a `.pa` extension.

## Source text and values

- Names and keywords are case-sensitive. A name starts with a letter or
  underscore and continues with letters, digits, or underscores.
- Whitespace separates tokens. Indentation and line breaks are for readability.
  A `#` outside a string starts a comment through the end of the line.
- Integers and decimals start with a decimal digit. Use `0.5` for a fraction
  below one. Unary `-` and `+` supply a sign. `float()` accepts additional
  forms such as `"1e3"`.
- Strings use single or double quotes. Supported escapes include newline
  (`\n`), tab (`\t`), escaped quotes, and an escaped backslash. A backslash
  before another character leaves that character as text.
- Boolean literals are `true` and `false`. A list uses square brackets and
  comma-separated expressions, including `[]` for an empty list.
- Reserved words are `say`, `function`, `return`, `import`, `if`, `else`,
  `end`, `while`, `true`, `false`, `null`, `elif`, `try`, `catch`, and `throw`. `and`, `or`, and `not` are also keywords. `repeat` is reserved.

## Expressions

| From tightest to loosest | Syntax |
| --- | --- |
| Primary expressions | Literals, variable names, calls, and grouped expressions |
| Indexing | `value[index]` |
| Exponentiation | `**` |
| Unary signs | `+value`, `-value` |
| Multiplicative operators | `*`, `/`, `//`, `%` |
| Additive operators | `+`, `-` |
| Comparison | `==`, `!=`, `<`, `<=`, `>`, `>=` |
| Logical negation | `not` |
| Logical conjunction | `and` |
| Logical disjunction | `or` |

Arithmetic at the same precedence groups left to right. Parentheses override
precedence. A comparison expression has one comparison operator. Operands and
call arguments evaluate left to right. Arithmetic and comparisons follow
Python value semantics. Division with `/` produces a floating-point result. Floor division rounds
toward negative infinity, so `-7 // 3` is `-3`. The remainder has the sign
of the divisor, so `-7 % 3` is `2`. These operators take integers and floats.
Power groups right to left. `2 ** 3 ** 2` is `512`, `-2 ** 2` is `-4`, and
`2 ** -2` is `0.25`. Power requires real results. To bound computation,
an integer power is rejected when the exponent times the bit length of the
base exceeds 1,000,000 bits (for absolute bases greater than 1).

An index starts at zero. Negative indexes count from the end. An invalid
index raises a runtime error. Use `len(value)` for the length of a string or
list. Indexing reads an item or character. Assignment targets a variable or an item in a named list or dictionary.

## Statements and functions

- `name = expression` assigns a value. `say expression` prints a value and a
  newline. Directly printed booleans appear as `true` or `false`.
- `if condition … else … end` chooses a block. `else` is optional.
  `while condition … end` reevaluates its condition before each iteration.
  Zero, empty strings, lists and dictionaries, `false`, and a missing return value are false
  in a condition.
- Define functions at the top level using `function name(parameters) … end`.
  Execute the definition before calling the function. Function names and
  variable names are looked up separately. Calls provide all required arguments. A trailing parameter can specify a default.
- Each call has its own local scope. Parameters and assignments inside a
  function are local. A read uses the local value if present and otherwise
  looks for a global variable.
- `return expression` exits the enclosing function, even inside a nested
  conditional or loop. A function with no executed return yields the
  missing value, printed as `null`. A call may also be a standalone statement.

## Built-in functions

| Function | Behavior |
| --- | --- |
| `len(value)` | Count characters, list items, or dictionary entries. |
| `int(value)` | Convert text or a numeric value to an integer. |
| `float(value)` | Convert text or a numeric value to a floating-point number. |
| `input()`, `input(prompt)` | Optionally print a prompt and read one line as text. Running out of lines raises a runtime error. |

A user-defined function of the same name takes precedence after its definition.
The browser reads the **Program input** box. The CLI and compiled Python read
standard input.

## Modules

Use `import "relative/path.pa"` at the top level. Paths are relative to the
importing file and must resolve within the entry file's directory. An import
includes a normalized path once at the position of its first import. Modules
share the program's top-level scope. Circular imports are errors.

The browser playground accepts sibling modules through its file picker.
The CLI supports nested module paths. Compiled Python includes imported
definitions and statements in a standalone script.


## Lists and loops added in 1.1

`for name in value … end` evaluates the iterable once and visits each list
item or string character in order. Each item is assigned in the current scope.
An empty iterable leaves the loop variable untouched. `break` exits the nearest
`for` or `while` loop and can appear inside a nested conditional.

`append(list, value)` mutates the list and returns the missing value. Other
variables referring to the same list see the added item. A loop iterating
over a list can see items appended before that iteration ends.


## Runtime errors added in 1.2

If execution fails, the first frame points to the failing operation in a
`.pa` file. Each following frame points to the call that entered the previous
function. Imported file names are preserved when running or compiling the
entry file. Compiled scripts embed the locations so the original files
are unnecessary when running the generated Python.


## Logic and loop continuation added in 1.4

`and`, `or`, and `not` produce boolean values using the same truth rules
as conditions. `and` skips its right operand when the left is false. `or`
skips its right operand when the left is true.

`continue` skips the remainder of the current iteration of the nearest
`for` or `while` loop. Like `for`, `in`, and `break`, it can still be used
as a variable or function name outside its control-flow syntax.


## Dictionaries added in 1.5

A dictionary maps keys to values, for example `{"name": "Ada", "score": 85}`.
Use `{}` for an empty dictionary and `student["name"]` to read a key.
Keys must be hashable values such as strings or numbers. Missing keys raise a
runtime error. A repeated key keeps the last assigned value.

Use `student["score"] = 90` to add or replace an entry. Indexed assignment also
works on list items, including chained indexes such as `student["scores"][0]`.
A `for` loop over a dictionary visits its keys in insertion order.


## Data built-ins added in 1.6

| Function | Behavior |
| --- | --- |
| `sum(items)` | Add the numbers in a list from left to right. An empty list returns `0`. |
| `min(items)` | Return the smallest number in a non-empty list. |
| `max(items)` | Return the largest number in a non-empty list. |
| `keys(record)` | Return a new list of dictionary keys in insertion order. An empty dictionary returns `[]`. |
| `get(record, key, default)` | Return the value for a key, or the supplied default if the key is absent. |

The numeric functions take a list of integers or decimals. Strings and
booleans raise a runtime error. An empty list raises an error for `min()`
and `max()`. The dictionary functions require a dictionary. `get()` requires
all three arguments and a hashable key. It keeps an existing value even if
that value is `0`, `false`, or the empty string.


## Text built-ins added in 1.7

| Function | Behavior |
| --- | --- |
| `trim(text)` | Remove leading and trailing Unicode whitespace. |
| `lower(text)`, `upper(text)` | Apply Unicode lowercase or uppercase conversion. |
| `split(text, separator)` | Split on a non-empty text separator. Adjacent separators and separators at the ends preserve empty fields. Splitting an empty string returns `[""]`. |
| `join(items, separator)` | Join a list of strings with the given text separator. An empty list returns the empty string. An empty separator is valid. |

These functions require text arguments where documented. `join()` also checks
that every item in its list is text. See the [name cleanup example](../examples/clean_names.pa).


## Module aliases

`import "module.pa" as module` initializes the file once per run in its own
namespace. Use `module.call()` or `module.value` for its top-level definitions.
An unaliased import continues to include statements in the importing scope.
See the [namespace example](../examples/namespaces.pa).


## Ranges and slices

`range(stop)` or `range(start, stop, step)` produces a list of integers
with an exclusive stop. The default step is 1, negative steps count down,
and a zero step raises an error. `sorted(items)` and `reverse(items)` return
new lists.

Use `items[start:stop]` or `items[start:stop:step]` on lists and strings.
Omitted bounds and negative offsets follow Python slice semantics. A list
slice can also be assigned using a list value.


## Standard modules

Import `"std/math"` with an alias for `abs()`, `round()`, and `sqrt()`.
Import `"std/json"` with an alias for `parse(text)` and `stringify(value)`.
The JSON module preserves Unicode and rejects non-finite numeric values.
See the [JSON student report](../examples/json_report.pa).


## Text and collection modules

Import `"std/text"`, `"std/list"`, or `"std/dict"` with an alias.

| Module | Function | Behavior |
|---|---|---|
| Text | `replace(text, old, new)` | Replace all occurrences and return a new string. |
| Text | `find(text, fragment)` | Return the first zero-based index, or `-1` when absent. |
| Text | `contains(text, fragment)` | Test whether a fragment occurs in a string. |
| Text | `starts_with(text, prefix)` | Test whether a string begins with the prefix. |
| Text | `ends_with(text, suffix)` | Test whether a string ends with the suffix. |
| List | `insert(items, index, value)` | Insert into the original list. Negative positions count from the end. Positions outside the list clamp to the beginning or end. |
| List | `pop(items, index)` | Remove and return the indexed item. The index defaults to `-1`. An invalid index raises an error. |
| List | `remove(items, value)` | Remove the first equal item and return `true`. Return `false` when absent. |
| List | `unique(items)` | Return a new list with the first occurrence of each value, in order. Accepts nested lists and dictionaries. |
| Dictionary | `has(record, key)` | Test whether the key exists, regardless of its value. |
| Dictionary | `remove(record, key, default)` | Remove and return the value, or return the fallback when absent. Without a fallback, a missing key produces the missing value. |
| Dictionary | `merge(left, right)` | Return a shallow copy with both sets of entries. Right-hand values win on shared keys. |

## Optional values and arguments

`null` represents a missing value. It is false in a condition, prints as
`null`, and corresponds to JSON `null`. A function that reaches the end
without returning also yields `null`. Use `type_of(value)` to get `null`,
`boolean`, `integer`, `float`, `string`, `list`, or `dictionary` as text.

Required parameters come before defaulted parameters. Omitted defaults are
evaluated in parameter order on each call, so a default can use earlier
parameters. Passing `null` explicitly supplies a value.

`elif` adds a condition to an `if` block. Only the first matching branch
runs. An optional `else` handles the remaining cases. See
[the invoice example](../examples/invoice_total.pa).

## Recoverable errors

Use `try … catch message … end` to handle runtime errors in a block. The
handler runs only if the protected block fails. The error variable receives
the message as a string in the current scope, and the handler may use normal
control flow. A failure in the handler can be caught by an enclosing block.
Syntax and import failures are reported before execution and cannot be caught.

Use `throw "reason"` to signal a runtime error. An unhandled error includes
the original `.pa` source location and its call stack. See
[the recoverable CSV example](../examples/recover_csv.pa).

## Queues, linked lists, and statistics

Import each module with an alias. Both collection types support `len()`.
Their `to_list()` functions make shallow snapshots suitable for JSON or CSV.
`type_of()` reports `queue` or `linked_list` for these collection values.

| Module | Function | Behavior |
|---|---|---|
| `std/queue` | `new(items)` | Create a FIFO queue. The initial list is optional. |
| Queue | `enqueue(queue, value)` | Add a value to the back of the existing queue. |
| Queue | `dequeue(queue)` | Remove and return the first value. An empty queue raises an error. |
| Queue | `peek(queue)` | Read the first value without removing it. An empty queue raises an error. |
| Queue | `to_list(queue)` | Return values from front to back. |
| `std/linked_list` | `new(items)` | Create a singly linked list. The initial list is optional. |
| Linked list | `append(linked, value)` | Add to the tail in constant time. |
| Linked list | `insert(linked, index, value)` | Insert at a zero-based position, including the position just past the last item. |
| Linked list | `remove(linked, index)` | Remove and return the item at that position. An invalid or negative index raises an error. |
| Linked list | `to_list(linked)` | Traverse the chain and return the values in order. You can also iterate directly with `for`. |
| `std/stats` | `mean(items)` | Return the arithmetic mean of a non-empty list of finite numbers. |
| Statistics | `median(items)` | Return the middle value, or the mean of the middle pair. Rejects empty input and non-finite numbers. |
| Statistics | `count_by(items, key)` | Count hashable values into a dictionary. With an optional key, count by that field in each record. An empty input yields an empty dictionary. |

See the [dispatch summary example](../examples/dispatch_summary.pa).

## Structured errors

Use `catch (error) … end` for a dictionary with `code`, `message`, `file`,
`line`, and `function`. Location fields are `null` when unavailable.
Plain `catch message` still receives the message string. Codes include
`csv_missing_columns`, `invalid_integer`, and `division_by_zero`.
Use `throw "code", "message"` to signal a custom code. The one-argument
form uses the code `thrown`.

See [the inventory example](../examples/structured_inventory.pa) for errors
that stop an import and errors that affect only the current row.
