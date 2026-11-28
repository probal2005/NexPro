# History of NexPro

NexPro began in August 2026 as a small programming language with a lexer,
parser, interpreter, and command-line interface. It grew into a language for
writing calculations and business rules, validating CSV and JSON data, and
turning programs into shareable browser tools.

## Inventor and creator

<img src="https://avatars.githubusercontent.com/u/197221117?v=4&amp;s=192" alt="Probal Dhali's GitHub profile image" width="144" height="144">

**Probal Dhali** created NexPro and maintains its public repository as
**@probal2005**. His public profile describes him as a computer science and
engineering student interested in AI, machine learning, and practical
problem-solving. The Python package credits him as the language's author.

[GitHub profile](https://github.com/probal2005) · [Portfolio](https://probaldhali.vercel.app/) · [Package authorship](pyproject.toml)

## Origins

The public repository opened on **4 August 2026**. The earliest commits
established tokenization, parsing, execution, and the CLI. The first working
implementation was marked **0.1.0**. The **0.2.0** and **0.3.0** milestones
added variables and numbers. The August work continued with a more complete
lexer, grammar, and abstract syntax tree.

[Initial project structure](https://github.com/probal2005/NexPro/commit/0c36f06) · [First working implementation](https://github.com/probal2005/NexPro/commit/84c8330) · [0.3.0 milestone](https://github.com/probal2005/NexPro/commit/47b76ac)

## Release milestones

| Version | What changed | Development record |
|---|---|---|
| **0.5–0.9** | Added compilation to standalone Python and launched the browser Playground. Functions, local variables, decisions, loops, lists, input, and modules expanded what a program could do. | [Compiler milestone](https://github.com/probal2005/NexPro/commit/3db1070) · [Playground launch](https://github.com/probal2005/NexPro/commit/483595f) |
| **1.0–2.0** | The stable CLI established a workflow for checking, running, and compiling programs. Dictionaries, text operations, tracing, diagnostics, and VS Code language support followed. | [1.0.0](https://github.com/probal2005/NexPro/releases/tag/v1.0.0) · [2.0.0](https://github.com/probal2005/NexPro/releases/tag/v2.0.0) |
| **2.1–3.0** | Aliased imports gave modules independent namespaces. Math and JSON libraries, project manifests, a test runner, and VS Code debugging helped organize and verify larger projects. | [3.0.0](https://github.com/probal2005/NexPro/releases/tag/v3.0.0) |
| **3.1–3.6** | Programs gained browser forms, CSV uploads and downloads, and shareable links that opened standalone tools. | [3.1.0](https://github.com/probal2005/NexPro/releases/tag/v3.1.0) · [3.6.0](https://github.com/probal2005/NexPro/releases/tag/v3.6.0) |
| **3.7–4.0** | Added floor division, remainder, and exponentiation, followed by default arguments, null, elif, and recoverable runtime errors. Queues, linked lists, and statistics broadened the standard library. | [3.7.0](https://github.com/probal2005/NexPro/releases/tag/v3.7.0) · [4.0.0](https://github.com/probal2005/NexPro/releases/tag/v4.0.0) |
| **4.1–4.6** | Structured errors and named arguments made validation easier to handle. Records gained required fields, defaults, type annotations, dot access, and dictionary conversion. | [4.1.0](https://github.com/probal2005/NexPro/releases/tag/v4.1.0) · [4.6.0](https://github.com/probal2005/NexPro/releases/tag/v4.6.0) |
| **4.7–4.9** | Records gained named business rules, atomic updates, and nested types with error paths such as `customer.email`. | [4.7.0](https://github.com/probal2005/NexPro/releases/tag/v4.7.0) · [4.9.0](https://github.com/probal2005/NexPro/releases/tag/v4.9.0) |
| **4.9.1 · 28 November 2026** | Adopted Apache 2.0, fixed form previews in imported modules, and preserved large integer results in browser reports. The Playground began serving its own pinned runtime, and browser tests joined GitHub CI. | [4.9.1](https://github.com/probal2005/NexPro/releases/tag/v4.9.1) |

## Projects and learning

By version 4.9.1, NexPro had **25 repository projects with live demos** and
**37 English lessons**. The project collection grew from small calculators
into a multi-warehouse fulfillment planner, a critical path scheduler, and a
booking optimizer. Learn NexPro follows a similar progression from a first
program to publishing a validated invoice tool.

[Live projects](https://nexpro-playground.vercel.app/#live-projects) · [Project source](projects/README.md) · [Learn NexPro](learn%20nexpro/README.md)

## Further reading

- [Changelog](docs/CHANGELOG.md) and [complete release history](https://github.com/probal2005/NexPro/releases)
- [Language reference](docs/language.md) and [grammar](docs/grammar.md)
- [Apache License 2.0](LICENSE)
