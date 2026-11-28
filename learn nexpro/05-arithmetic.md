# 05. Integers, floats, and arithmetic

[← Previous lesson](04-input-output.md) · [Course index](README.md) · [Next lesson →](06-comparisons.md)

NexPro uses seven arithmetic symbols. Plus and minus also work as unary signs.

## Types and syntax

| Type | Syntax | Definition |
|---|---|---|
| Addition and unary plus | `5 + 3`, `+5` | Adds two values or applies a positive sign. |
| Subtraction and unary minus | `5 - 3`, `-5` | Subtracts a value or negates a number. |
| Multiplication | `5 * 3` | Multiplies two values. |
| Division | `7 / 2` | Divides and returns a float. |
| Floor division and remainder | `7 // 3`, `7 % 3` | Return the quotient rounded down and the remainder. |
| Power | `2 ** 3` | Raises a number to a power and groups right to left. |
| Precedence | `(2 + 3) * 4` | Parentheses set the order of evaluation. |

## When and why to use it

Use arithmetic to calculate totals, convert units, or find an average.

**Advantages.** Short expressions make formulas easy to read.

**Limitations and common mistakes.** Division by zero raises an error. Store money in integer cents when you need exact arithmetic. Power is restricted to real results.

## Try it

Paste this code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**. [Download the example .pa file](examples/05-arithmetic.pa)

```text
say 2 + 3 * 4
say (2 + 3) * 4
say 7 / 2
say -5 + 3
```

**Expected result**

```text
14
20
3.5
-2
```

## Exercise

How many items are in 7 boxes of 3?

<details>
<summary>Show the answer</summary>

`say 7 * 3` prints `21`.

</details>

[← Previous lesson](04-input-output.md) · [Course index](README.md) · [Next lesson →](06-comparisons.md)
