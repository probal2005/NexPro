# 01. Your first .pa program

[Course index](README.md) · [Next lesson →](02-variables.md)

NexPro source is UTF-8 text, usually saved in a file with the .pa extension.

## Types and syntax

| Type | Syntax | Definition |
|---|---|---|
| Comment | `# note` | Explains the code through the end of the line. |
| Output | `say expression` | Prints a value followed by a newline. |
| String literal | `"Hello"` | Represents text inside quotes. |

## When and why to use it

Start with a short calculation or message to check that your setup works. To run locally, save the program as hello.pa and run `nexpro run hello.pa`.

**Advantages.** You get immediate feedback from a small program.

**Limitations and common mistakes.** Names are case-sensitive. A # inside quotes is part of the string.

## Try it

Paste this code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**. [Download the example .pa file](examples/01-first-program.pa)

```text
# First program
say "Hello, NexPro!"
say 2 + 3
```

**Expected result**

```text
Hello, NexPro!
5
```

## Exercise

Add a line that prints your name.

<details>
<summary>Show the answer</summary>

For example, `say "Ada"`.

</details>

[Course index](README.md) · [Next lesson →](02-variables.md)
