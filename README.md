# NexPro

NexPro is a small programming language for `.pa` source files. It comes with an
interpreter and a compiler that generates standalone Python scripts.

## Get started

Try the [online playground](https://nexpro-playground.vercel.app/) or install
the CLI with Python 3.11 or later. Download `nexpro-1.3.0-py3-none-any.whl` from
the [1.3.0 release](https://github.com/probal2005/NexPro/releases/tag/v1.3.0).
From your download directory, run:

```sh
python -m pip install ./nexpro-1.3.0-py3-none-any.whl
nexpro version
```

You can also run `python -m pip install .` from a checkout of this repository.
See the [installation guide](docs/HELP.md) for virtual environments and
Windows commands.

Create a UTF-8 file named `hello.pa` with this line:

```text
say "Hello NexPro!"
```

Then check, run, and compile it:

```sh
nexpro check hello.pa
nexpro run hello.pa
nexpro compile hello.pa -o hello.py
python hello.py
```

Both run commands print `Hello NexPro!`. The generated script needs Python
and includes any imported modules. Without `-o`, compilation writes a
sibling file with the `.py` extension.

Follow the [first-program tutorial](docs/tutorial.md) to build a small score
calculator. See the [language reference](docs/language.md) and the
[grammar](docs/grammar.md) for the language syntax and behavior.

For `.pa` highlighting and syntax checks inside VS Code, install the
[NexPro extension](editors/vscode/README.md).

## Language

```text
# Print text and evaluate expressions
name = "NexPro"
say name
say 2 + 3 * 4
say (2 + 3) * 4
```

NexPro supports assignments, `say`, strings, integers, decimals, comments,
and the four basic arithmetic operators. Multiplication and division bind more
tightly than addition and subtraction. Parentheses override that order.

### Functions and scope

```text
rate = 2

function total(quantity, price)
    subtotal = quantity * price
    return subtotal + rate
end

say total(3, 5)
```

Define a function before calling it. Parameters and assignments inside a
function are local to that call. Functions can also read global variables.
A local assignment shadows a global of the same name. Use `return expression`
to pass a value back to the caller. A function that reaches `end` returns
`None` when printed. Use `+` or `-` before an expression for unary signs.

See [functions](examples/functions.pa), [scope](examples/scope.pa),
[temperature conversion](examples/temperature.pa), and [greeting](examples/greeting.pa).

### Decisions and loops

Use `if` with an optional `else` to choose a block, and `while` to repeat a
block while its condition holds. Both end with `end`.

```text
number = 1
while number <= 3
    if number == 2
        say "two"
    else
        say number
    end
    number = number + 1
end
```

Comparisons (`==`, `!=`, `<`, `<=`, `>`, `>=`) evaluate after arithmetic and
produce `true` or `false`. A condition treats zero, an empty string or list,
`false`, and a missing return value as false. Other values are true. Use **Stop** in
the playground or **Ctrl+C** in your terminal to interrupt a running loop.

See the [grade calculator](examples/grades.pa), [multiplication table](examples/multiplication_table.pa),
and [sum from 1 to 10](examples/sum_1_to_10.pa).

### Lists and program input

Write a list as `[10, 20, 30]` or use `[]` for an empty list. Indexes start at
zero. An index of `-1` reads the last item. `len()` returns the length of a
list or string. Indexing also works on strings and nested lists.

`input()` reads one line as text. Use `int(text)` or `float(text)` to convert
it to a number. In the browser, enter the lines in **Program input** before
running. The CLI and generated Python read from standard input.

```sh
printf '70\n85\n100\n' | nexpro run examples/scores.pa
```

See [lists](examples/lists.pa), [score statistics](examples/scores.pa), and
[a greeting with input](examples/input.pa).

### Syntax checks and modules

```sh
nexpro check examples/imports.pa
nexpro run examples/imports.pa
nexpro compile examples/imports.pa -o imports.py
```

`check` validates the entry file and its imports without executing any code.
Syntax errors show the filename, line, column, and a caret under the source.

Use `import "math_utils.pa"` at the top level. Paths are relative to the file
containing the import and stay within the entry file's directory. An imported
file is included once at its first import. Its functions and variables are
available in the program's global scope. Circular imports produce an error.
Compiled Python includes the modules and can run by itself.

In the playground, select **Import math functions** for a preloaded example,
or attach your own sibling `.pa` files under **Module files**. Use **Check
syntax** to check the editor and its imports without running the program.

The `numbers.pa`, `string.pa`, `escape.pa`, `operators.pa`, and `keywords.pa`
examples are lexer fixtures. The `error.pa` fixture demonstrates invalid input.

## Tests

Install NexPro and pytest in the same Python environment, then run
`python -m pytest -q` from the repository root.

## Browser playground

The playground runs the repository's Python implementation in a browser worker
using Pyodide. Vercel builds the static site from the repository root using
`node web/build.mjs`; the generated site is placed in `dist/`.
