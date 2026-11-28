# 04. Input, output, and conversion

[← Previous lesson](03-data-types.md) · [Course index](README.md) · [Next lesson →](05-arithmetic.md)

The input function reads one line of text. Convert text before using it in numeric calculations.

## Types and syntax

| Type | Syntax | Definition |
|---|---|---|
| Read | `input()` or `input("Name: ")` | Reads one line and optionally prints a prompt. |
| Print | `say value` | Prints a value. |
| Integer conversion | `int("12")` | Converts text or a number to an integer. |
| Float conversion | `float("1.5")` | Converts text or a number to a float. |
| Length | `len(value)` | Counts characters, list items, or dictionary entries. |

## When and why to use it

Use line-based input for a calculator or command-line exercise. Enter 4 and 2.5 on separate lines in Program input.

**Advantages.** The same program can run with different input values.

**Limitations and common mistakes.** Invalid numeric text or too few input lines raises a runtime error.

## Try it

Paste this code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**. [Download the example .pa file](examples/04-input-output.pa)

Enter these two lines in **Program input**.

```text
4
2.5
```

```text
quantity = int(input())
price = float(input())
say quantity * price
```

**Expected result**

```text
10.0
```

## Exercise

What happens if the first input is 8?

<details>
<summary>Show the answer</summary>

The program prints `20.0`.

</details>

[← Previous lesson](03-data-types.md) · [Course index](README.md) · [Next lesson →](05-arithmetic.md)
