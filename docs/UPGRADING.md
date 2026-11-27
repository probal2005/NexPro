# Upgrade to NexPro 2.0

NexPro 2.0 keeps the existing `.pa` syntax, relative imports, and CLI commands.
Existing programs can keep their entry files and module paths. Existing
user-defined functions still take precedence over built-ins.

## Update the CLI and editor

1. Download and install the 2.0 Python wheel. [Release downloads](https://github.com/probal2005/NexPro/releases/tag/v2.0.0)
2. Run `nexpro version` and confirm it prints `NexPro 2.0.0`.
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
