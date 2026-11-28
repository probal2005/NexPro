# Changelog

All notable changes to NexPro will be documented here.

---

## v4.9.1

- Forms declared in aliased modules now render and receive the submitted values.
- Browser numeric fields reject integers outside the exact input range. Project
  reports preserve large integer results and their raw JSON digits.
- The site serves its pinned Pyodide runtime and CI builds and tests the browser.
- Added Apache 2.0 licensing and an invoice workflow to Learn NexPro.

## v4.7–4.9

- Added named record rules, atomic updates, and nested record types.
- Added recursive dictionary conversion with field paths in errors.

## v4.4–4.6

- Added typed record fields and made dot and index writes use the same checks.
- Added conversions between records and dictionaries in `std/record`.

## v4.1–4.3

- Added structured catches, named arguments, and fixed-field record constructors.

## v3.7–4.0

- Added floor division, remainder, exponentiation, and text, list, and dictionary modules.
- Added null, default arguments, elif, and recoverable runtime errors.
- Added queues, linked lists, and statistics.

## v3.1–3.6

- Added browser forms, CSV processing and downloads, and shareable standalone tools.
- Added dropdowns, checkboxes, field validation, and CSV upload fields.

## v3.0.0

- Added aliased modules with isolated globals, slices, ranges, and standard math and JSON modules.
- Added VS Code source debugging, completion, hover help, and cross-platform CLI validation.
- Added project manifests, a starter command, and a NexPro test runner.
- Added execution benchmarks and regression tests for upgrading from 2.0.

## v2.0.0

Stable release of the text functions, editor diagnostics, and execution
tracing introduced in 1.7 through 1.9. See the [upgrade guide](UPGRADING.md)
for compatibility and tooling details.

## v1.9.0

Added execution tracing in the CLI, browser playground, and VS Code.

## v1.8.0

Added JSON syntax diagnostics and VS Code checks on save.

## v1.7.0

Added `trim()`, `lower()`, `upper()`, `split()`, and `join()`.

## v1.6.0

Added `sum()`, `min()`, `max()`, `keys()`, and `get()`, plus a student report example.

## v1.5.0

Added dictionaries and indexed assignment for dictionary entries and list items.

## v1.4.0

Added short-circuit logical operators and `continue`.

## v1.3.0

Added a VS Code extension with syntax highlighting and the **Check Syntax** command.

## v1.2.0

Runtime errors include NexPro file names, line numbers, and function call frames.

## v1.1.0

Added `for`, `break`, and `append()`.

## v1.0.0

First stable release. The language reference, grammar, installation guide, and
tutorial describe the supported 1.0 behavior.

- Interpret, syntax-check, and compile `.pa` programs with the CLI or playground.
- Use functions, control flow, lists, program input, and relative module imports.
- Install the universal Python wheel from the GitHub release.

## v0.3.0

Release Date:
2026

## Added

- Professional CLI

- Character Based Lexer

- Token System

- AST (Abstract Syntax Tree)

- Recursive Descent Parser

- Runtime Environment

- Interpreter

- Variables

- Strings

- Numbers

- Arithmetic Operators

- Parentheses

- Operator Precedence

- Examples

- Tests

- Professional Error System

---

Initial Stable Release.