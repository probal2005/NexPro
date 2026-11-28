# 13. Functions, parameters, and scope

[← Previous lesson](12-dictionaries.md) · [Course index](README.md) · [Next lesson →](14-imports.md)

A function is a named block of code that can be called more than once.

## Types and syntax

| Type | Syntax | Definition |
|---|---|---|
| Definition | `function total(price, quantity) … end` | Names the function and declares its parameters. |
| Call | `total(50, 3)` | Supplies arguments and executes the function. |
| Return | `return price * quantity` | Passes a result back to the caller. |
| Local scope | Assignment inside a function | Keeps each call's local values separate. |
| Global lookup | Read a top-level variable | Falls back to the global value when no local value exists. |

## When and why to use it

Put repeatable calculations or validation rules into functions.

**Advantages.** A small function is easier to reuse and test independently.

**Limitations and common mistakes.** Execute the definition before calling. Supply all required arguments. A trailing parameter such as `fee = 0` can have a default. A missing return produces `null`.

## Try it

Paste this code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**. [Download the example .pa file](examples/13-functions.pa)

```text
tax = 5
function total(price, quantity)
    subtotal = price * quantity
    return subtotal + tax
end
say total(50, 3)
say total(25, 2)
```

**Expected result**

```text
155
55
```

## Exercise

What changes if tax is 10?

<details>
<summary>Show the answer</summary>

Both results increase by 5.

</details>

[← Previous lesson](12-dictionaries.md) · [Course index](README.md) · [Next lesson →](14-imports.md)
