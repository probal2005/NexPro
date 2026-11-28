# Install and use NexPro 3.2

Use Python 3.11 or later. Download `nexpro-3.2.0-py3-none-any.whl` from the
[GitHub release](https://github.com/probal2005/NexPro/releases/tag/v3.2.0)
and open a terminal in the download directory.

## macOS and Linux

```sh
python3 -m venv .venv
.venv/bin/python -m pip install ./nexpro-3.2.0-py3-none-any.whl
source .venv/bin/activate
nexpro version
```

## Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install .\nexpro-3.2.0-py3-none-any.whl
.\.venv\Scripts\nexpro.exe version
```

The version command prints `NexPro 3.2.0`. On Windows, use
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

### Build a browser tool with NexPro

Open **Bill Splitter form** or **Freelance Quote form** in the playground examples and click **Preview tool**. Edit the generated form and click **Calculate**.

- `number_field(label, default, minimum)` accepts decimal input. The minimum is optional.
- `text_field(label, default)` accepts text. The default is optional.
- `result(label, value)` displays a labeled result. Each input field needs a unique label.

When you run a tool from the command line or compile it to Python, the fields return their defaults and results print to standard output.

### Import and export CSV

Select **Inventory reorder from CSV** and click **Run code** to try the sample.
To use your own file, choose **Open CSV** and run again. **Download CSV output**
saves the program's output. The inventory example expects `sku,stock,minimum,target`
columns and writes `sku,quantity`.

Import `"std/csv" as csv` for `csv.parse(text)` and `csv.stringify(rows)`.
Parsing uses the first row as column names and returns cell values as text.
Writing uses the first dictionary's key order and requires the same columns in
each row. In the playground, `json.parse(input())` reads an uploaded CSV as text.
