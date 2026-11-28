# 15. std/math — absolute value, rounding, and square roots

[← Previous lesson](14-imports.md) · [Course index](README.md) · [Next lesson →](16-json.md)

The standard math module provides three functions.

## Types and syntax

| Type | Syntax | Definition |
|---|---|---|
| Absolute value | `math.abs(-7)` | Returns the magnitude of a number. |
| Round | `math.round(12.346, 2)` | Rounds to the requested decimal places. |
| Square root | `math.sqrt(81)` | Returns the square root of a nonnegative number. |

## When and why to use it

Round a report value for display or use abs to measure a stock discrepancy.

**Advantages.** Common calculations are available without writing your own implementations.

**Limitations and common mistakes.** Square root requires a nonnegative input. Rounding a float does not make it suitable for exact money storage.

## Try it

Paste this code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**. [Download the example .pa file](examples/15-math.pa)

```text
import "std/math" as math
say math.abs(-7)
say math.round(12.346, 2)
say math.sqrt(81)
```

**Expected result**

```text
7
12.35
9.0
```

## Exercise

Print the square root of 144.

<details>
<summary>Show the answer</summary>

`say math.sqrt(144)` prints `12.0`.

</details>

[← Previous lesson](14-imports.md) · [Course index](README.md) · [Next lesson →](16-json.md)
