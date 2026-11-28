# 07. Booleans and logical operators

[← Previous lesson](06-comparisons.md) · [Course index](README.md) · [Next lesson →](08-conditionals.md)

Logical operators combine or invert conditions and return booleans.

## Types and syntax

| Type | Syntax | Definition |
|---|---|---|
| And | `a and b` | True when both conditions are true. |
| Or | `a or b` | True when at least one condition is true. |
| Not | `not a` | Inverts the condition. |
| Truth testing | `not []` | Zero, empty strings, empty lists, and empty dictionaries count as false. |

## When and why to use it

Require both available stock and approval before releasing an order.

**Advantages.** Short-circuit evaluation skips the right operand when the left operand already determines the result.

**Limitations and common mistakes.** Use named conditions or parentheses when a long logical expression is hard to read.

## Try it

Paste this code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**. [Download the example .pa file](examples/07-logic.pa)

```text
stock = 4
approved = true
say stock > 0 and approved
say stock == 0 or not approved
say stock != 0 and 12 / stock > 2
```

**Expected result**

```text
true
false
true
```

## Exercise

What is the final output if stock is 0?

<details>
<summary>Show the answer</summary>

`false`. The division expression is skipped.

</details>

[← Previous lesson](06-comparisons.md) · [Course index](README.md) · [Next lesson →](08-conditionals.md)
