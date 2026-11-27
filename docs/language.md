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
  `end`, `while`, `true`, and `false`. `and`, `or`, and `not` are also keywords. `repeat` is reserved.

## Expressions

| From tightest to loosest | Syntax |
| --- | --- |
| Primary expressions | Literals, variable names, calls, and grouped expressions |
| Indexing | `value[index]` |
| Unary signs | `+value`, `-value` |
| Multiplicative operators | `*`, `/` |
| Additive operators | `+`, `-` |
| Comparison | `==`, `!=`, `<`, `<=`, `>`, `>=` |
| Logical negation | `not` |
| Logical conjunction | `and` |
| Logical disjunction | `or` |

Arithmetic at the same precedence groups left to right. Parentheses override
precedence. A comparison expression has one comparison operator. Operands and
call arguments evaluate left to right. Arithmetic and comparisons follow
Python value semantics. Division produces a floating-point result.

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
  variable names are looked up separately. Calls supply one argument per
  parameter.
- Each call has its own local scope. Parameters and assignments inside a
  function are local. A read uses the local value if present and otherwise
  looks for a global variable.
- `return expression` exits the enclosing function, even inside a nested
  conditional or loop. A function with no executed return yields the
  missing value, printed as `None`. A call may also be a standalone statement.

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
