# Upgrade to NexPro 3.0

NexPro 3.0 keeps the existing `.pa` syntax, relative imports, and CLI commands.
Existing programs can keep their entry files and module paths. Existing
user-defined functions still take precedence over built-ins.

## Update the CLI and editor

1. Download and install the 3.0 Python wheel. [Release downloads](https://github.com/probal2005/NexPro/releases/tag/v3.0.0)
2. Run `nexpro version` and confirm it prints `NexPro 3.0.0`.
3. Install the matching VSIX if you use VS Code. [Extension guide](../editors/vscode/README.md)

Previously generated Python scripts remain standalone. To use new language
features, compile the `.pa` source again with the updated CLI.

## Check and trace a program

```sh
nexpro check --json examples/imports.pa
nexpro run --trace examples/imports.pa
```

The JSON check prints one object to standard output. `ok` is a boolean and
`diagnostics` is an array. A diagnostic has a `message` and includes
`filename`, `line`, and `column` when the error has a source location.
Line and column numbers start at one. A failed check returns exit code 1.

Trace lines go to standard error, while program output stays on standard
output. Each trace line gives the source file, line, and function name.
The playground displays traces separately and keeps the first 500 statements.

VS Code checks saved `.pa` files in trusted workspaces. Disable automatic
checks with `nexpro.checkOnSave`, or run **NexPro: Check Syntax** from the
Command Palette. **NexPro: Run with Trace** starts the program in the
integrated terminal.


## New tools in 2.1–2.5

Existing unaliased imports still share their importing scope. Use an alias
when modules contain names that should stay separate. Ranges, slices, and
the math and JSON modules are available on all execution paths.

The VS Code extension offers completion and hover help for built-ins and
standard modules. For breakpoints and variable inspection, launch the NexPro
debugger. The debugger uses the interpreter and handles program input from
the launch configuration.


## Projects and tests

Run `nexpro init my-project` to create `main.pa` and `nexpro.toml`. The
manifest's `[project]` table sets `entry` and `tests` relative to the project
directory. From that project, `nexpro run`, `nexpro check`, and `nexpro compile`
use the configured entry when you omit the filename.

Write `test_*.pa` files under the configured test directory. Run `nexpro test`
to execute each file independently. A false `assert expression` fails the
test and reports its source location. Test files can import other project
files using relative paths.

To debug a failing test, open the test file in VS Code, put a breakpoint on
the failing assertion, and start the NexPro debugger. Step In, Step Over,
and Continue are available in the debug toolbar. Program input can be
supplied with the launch configuration's `input` string.

Run `python scripts/benchmark.py` from a checkout with NexPro installed
to measure list creation, multi-file imports, and a loop workload.

On Windows, NexPro CLI input and output and standalone generated Python use UTF-8.
