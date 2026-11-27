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

NexPro 0.5 supports assignments, `say`, strings, integers, decimals, comments,
and the four basic arithmetic operators. Multiplication and division bind more
tightly than addition and subtraction. Parentheses override that order.

The `numbers.pa`, `string.pa`, `escape.pa`, `operators.pa`, and `keywords.pa`
examples are lexer fixtures. The `error.pa` fixture demonstrates invalid input.

## Tests

Install NexPro and pytest in the same Python environment, then run
`python -m pytest -q` from the repository root.

## Browser playground

The playground runs the repository's Python implementation in a browser worker
using Pyodide. Vercel builds the static site from the repository root using
`node web/build.mjs`; the generated site is placed in `dist/`.
