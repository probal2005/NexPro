# 06. Comparison operators

[← Previous lesson](05-arithmetic.md) · [Course index](README.md) · [Next lesson →](07-logic.md)

Comparing two operands produces a boolean value.

## Types and syntax

| Type | Syntax | Definition |
|---|---|---|
| Equality | `==`, `!=` | Equal to or not equal to. |
| Lower bound checks | `<`, `<=` | Less than or less than or equal to. |
| Upper bound checks | `>`, `>=` | Greater than or greater than or equal to. |

## When and why to use it

Test whether stock has reached a reorder threshold or a score has reached a passing mark.

**Advantages.** An inclusive operator makes it clear whether a boundary value counts.

**Limitations and common mistakes.** Use one comparison operator per comparison expression. Combine two comparisons with and when checking a range.

## Try it

Paste this code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**. [Download the example .pa file](examples/06-comparisons.pa)

```text
stock = 4
say stock == 4
say stock != 4
say stock < 5
say stock <= 4
say stock > 3
say stock >= 5
```

**Expected result**

```text
true
false
true
true
true
false
```

## Exercise

How can you check that stock is between 3 and 6, inclusive?

<details>
<summary>Show the answer</summary>

`stock >= 3 and stock <= 6`.

</details>

[← Previous lesson](05-arithmetic.md) · [Course index](README.md) · [Next lesson →](07-logic.md)
