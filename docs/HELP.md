# Install and use NexPro 2.8

Use Python 3.11 or later. Download `nexpro-2.8.0-py3-none-any.whl` from the
[GitHub release](https://github.com/probal2005/NexPro/releases/tag/v2.8.0)
and open a terminal in the download directory.

## macOS and Linux

```sh
python3 -m venv .venv
.venv/bin/python -m pip install ./nexpro-2.8.0-py3-none-any.whl
source .venv/bin/activate
nexpro version
```

## Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install .\nexpro-2.8.0-py3-none-any.whl
.\.venv\Scripts\nexpro.exe version
```

The version command prints `NexPro 2.8.0`. On Windows, use
`.\.venv\Scripts\nexpro.exe` in place of `nexpro` if the environment is inactive.
Use `py -3` for Python commands if `python` is unavailable.

## CLI commands

| Command | Behavior |
| --- | --- |
| `nexpro run file.pa` | Interpret the program. Add `--trace` to print executed source locations to standard error. |
| `nexpro check file.pa` | Validate syntax and imports without executing statements. Add `--json` for editor integration. |
| `nexpro compile file.pa -o file.py` | Generate a Python script. Omit `-o` to replace the source extension with `.py` in the output path. |
| `nexpro version` | Print the installed version. |
| `nexpro help` | List available commands. Use `--help` after a command for its options. |

To install from a repository checkout, run `python -m pip install .` from its
root inside your environment. The [tutorial](tutorial.md) starts with a
Hello World program you can create in any directory.
