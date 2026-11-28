# 03. Data types and literals

[← Previous lesson](02-variables.md) · [Course index](README.md) · [Next lesson →](04-input-output.md)

NexPro 3.8 has seven value types you can write directly as literals.

## Types and syntax

| Type | Syntax | Definition |
|---|---|---|
| Integer | `12` | A whole number. |
| Float | `7.5` | A floating-point number. |
| String | `"Ada"` | Text. |
| Null | `null` | A missing value. |
| Boolean | `true`, `false` | A truth value. |
| List | `[3, 4]` | An ordered collection. |
| Dictionary | `{"stock": 4}` | A collection that associates keys with values. |

## When and why to use it

Use an integer for stock, a string for the product name, and a dictionary to keep both values together.

**Advantages.** The right type makes the intended operations clearer.

**Limitations and common mistakes.** An operation may fail if the type is incompatible. A function that finishes without a return has a missing result, displayed as `null`. Use `type_of(value)` to query a value’s type.

## Try it

Paste this code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**. [Download the example .pa file](examples/03-data-types.pa)

```text
item = {"name": "Rice", "stock": 4}
say item["name"]
say item["stock"] > 0
say len([4, 5])
```

**Expected result**

```text
Rice
true
2
```

## Exercise

Change the stock to 0 and run again.

<details>
<summary>Show the answer</summary>

The second output line is `false`.

</details>

[← Previous lesson](02-variables.md) · [Course index](README.md) · [Next lesson →](04-input-output.md)
