# NexPro

NexPro is a small programming language for `.pa` source files. It comes with an
interpreter and a compiler that generates standalone Python scripts.

## Install

With Python 3.11 or later, run this from the repository root:

```sh
python -m pip install .
```

## Run or compile a program

```sh
nexpro run examples/hello.pa
nexpro compile examples/math.pa -o math_program.py
python math_program.py
```

Without `-o`, the compiler replaces the source extension with `.py` in the
output path. The generated script runs with Python alone. Use `nexpro help` or
`nexpro compile --help` for command options.

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

The `numbers.pa`, `string.pa`, `escape.pa`, `operators.pa`, and `keywords.pa`
examples are lexer fixtures. The `error.pa` fixture demonstrates invalid input.

## Tests

Install NexPro and pytest in the same Python environment, then run
`python -m pytest -q` from the repository root.

## Browser playground

The playground runs the repository's Python implementation in a browser worker
using Pyodide. Vercel builds the static site from the repository root using
`node web/build.mjs`; the generated site is placed in `dist/`.
