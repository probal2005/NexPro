<img src="web/nexpro-icon.png" alt="" width="64" height="64" align="left">

# NexPro

NexPro is a small programming language for turning calculations and rules into
shareable browser tools. Write a `.pa` file, generate a form from its field
declarations, or use the same program from a terminal or as standalone Python.

[Online Playground](https://nexpro-playground.vercel.app/) ·
[Latest release](https://github.com/probal2005/NexPro/releases/latest) ·
[Language reference](docs/language.md) ·
[VS Code extension](editors/vscode/README.md)

## Learn NexPro

Follow the [Learn NexPro course](learn%20nexpro/README.md) from
your first `.pa` program to a shareable CSV inventory tool.

## Built with NexPro

Explore [10 runnable NexPro projects](projects/README.md), including group
expense settlement, student report cards, and tournament standings. Each
project includes a live form, its `.pa` source, a sample input, and the expected output.

[Try the Bill Splitter web demo](https://nexpro-playground.vercel.app/projects/bill-splitter/) ·
[Read its NexPro source](projects/bill-splitter/main.pa)

[Try the Order Dispatch Checker](https://nexpro-playground.vercel.app/projects/order-dispatch/) ·
[Read its NexPro rules](projects/order-dispatch/main.pa)

## Build a tool

Try **Bill Splitter form**, **Freelance Quote form**, or **Inventory reorder from CSV**
in the playground. Select **Preview tool** to generate a form from `.pa` code, or
**Run code** to process a CSV. **Share tool** creates a link to a standalone form. **Share code** opens the
same source and attached modules in the playground.

[Try the Inventory Reorder tool](https://nexpro-playground.vercel.app/tool.html?example=inventory) ·
[Browser tool guide](docs/HELP.md#build-a-browser-tool-with-nexpro)

## Quick start

### Try it in your browser

Open the [playground](https://nexpro-playground.vercel.app/), choose **Hello world**
from **Examples**, and select **Run code**. Use **Check syntax** to validate a
program or **Compile to Python** to preview and download the generated script.

Enter one line per `input()` call in **Program input**. Attach imported sibling
`.pa` files under **Module files**. Select **Stop** to interrupt a running program.

### Install the CLI

Use Python 3.11 or later. Download the wheel from the
[4.0.0 release](https://github.com/probal2005/NexPro/releases/tag/v4.0.0),
then run these commands from your download directory.

```sh
python -m pip install ./nexpro-4.0.0-py3-none-any.whl
nexpro version
```

See the [installation guide](docs/HELP.md) for virtual environments and Windows
commands. To install from a repository checkout, run `python -m pip install .`
from the repository root.

### Write your first program

Save this as `hello.pa` in UTF-8.

```text
say "Hello NexPro!"
```

```sh
nexpro check hello.pa
nexpro run hello.pa
nexpro compile hello.pa -o hello.py
python hello.py
```

The interpreter and the generated script both print `Hello NexPro!`. The
generated script runs with Python alone, including when the NexPro source
imports other `.pa` files.

## What NexPro supports

| Feature | Example |
| --- | --- |
| Variables, arithmetic, and operator precedence | [Arithmetic](examples/math.pa) |
| Functions, parameters, return values, and local scope | [Functions](examples/functions.pa) · [Scope](examples/scope.pa) |
| Conditions, short-circuit logic, and loops with `break` and `continue` | [Grade calculator](examples/grades.pa) · [Score filter](examples/score_filter.pa) |
| Lists, dictionaries, and indexed assignment | [Lists](examples/lists.pa) · [Student scorecard](examples/scorecard.pa) |
| Text input, numeric conversion, and list growth with `append()` | [Variable-length score input](examples/score_series.pa) |
| Numeric summaries and dictionary helpers | [Student report](examples/student_report.pa) |
| Unicode text cleanup, splitting, and joining | [Clean up a list of names](examples/clean_names.pa) |
| Relative imports and independent module namespaces | [Import math functions](examples/imports.pa) · [Module aliases](examples/namespaces.pa) |
| Ranges, slicing, and list sorting | [Ranked scores](examples/ranked_scores.pa) |
| Standard math and JSON modules | [JSON student report](examples/json_report.pa) |

The example below stores a student's name and scores in a dictionary, then uses
a function and a loop to calculate the average.

```text
function average(scores)
    total = 0
    for score in scores
        total = total + score
    end
    return total / len(scores)
end

student = {"name": "Ada", "scores": [70, 85, 100]}
say student["name"]
say average(student["scores"])
```

```text
Ada
85.0
```

## Command reference

| Command | What it does |
| --- | --- |
| `nexpro run file.pa` | Run a program. Add `--trace` to see executed source locations on standard error. |
| `nexpro check file.pa` | Check syntax and imports without running the program. Add `--json` for editor integration. |
| `nexpro compile file.pa -o file.py` | Generate standalone Python. Omit `-o` to write a sibling `.py` file. |
| `nexpro init my-project` | Create a starter file and project manifest. |
| `nexpro test` | Run a project’s `test_*.pa` files. |
| `nexpro version` | Print the installed version. |
| `nexpro help` | List the available commands. |

Syntax diagnostics show the source file, line, and column. Runtime errors in
the interpreter and generated Python report NexPro source locations and
function call frames. Execution traces show statements as they run, including
statements inside imported functions. In the browser, enable **Trace execution**
before selecting **Run code**.

## Documentation and editor support

- [First-program tutorial](docs/tutorial.md) and [upgrade guide](docs/UPGRADING.md)
- [Language reference](docs/language.md) and [formal grammar](docs/grammar.md)
- [VS Code installation and setup](editors/vscode/README.md) for `.pa` syntax highlighting and the **NexPro: Check Syntax** and **NexPro: Run with Trace** commands
- [Changelog](docs/CHANGELOG.md) and [release downloads](https://github.com/probal2005/NexPro/releases)

## Development

From the repository root, install the project and run the test suite.

```sh
python -m pip install . pytest
python -m pytest -q
```

The language implementation lives in [`nexpro/`](nexpro/), the browser editor
in [`web/`](web/), and the VS Code extension in
[`editors/vscode/`](editors/vscode/). The playground runs NexPro through
Pyodide in a browser worker. Build the static site with `node web/build.mjs`.
The build output goes in `dist/`.
