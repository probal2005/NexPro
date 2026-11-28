# 02. Variables and assignment

[← Previous lesson](01-first-program.md) · [Course index](README.md) · [Next lesson →](03-data-types.md)

A variable is a name you can use to read or update a value.

## Types and syntax

| Type | Syntax | Definition |
|---|---|---|
| Assignment | `price = 50` | Associates a value with a name. |
| Reassignment | `price = price + 5` | Reads the current value and stores a new one. |
| Identifier | `unit_price` | Starts with a letter or underscore. Later characters may include digits. |

## When and why to use it

Store a unit price, quantity, and total under meaningful names.

**Advantages.** You can reuse a value and change it in one place.

**Limitations and common mistakes.** Reading a name before it has a value raises a runtime error. Variables have no static type declarations.

## Try it

Paste this code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**. [Download the example .pa file](examples/02-variables.pa)

```text
price = 50
quantity = 3
price = price + 5
say price * quantity
```

**Expected result**

```text
165
```

## Exercise

What is the total if quantity is 4?

<details>
<summary>Show the answer</summary>

`55 * 4` gives `220`.

</details>

[← Previous lesson](01-first-program.md) · [Course index](README.md) · [Next lesson →](03-data-types.md)
