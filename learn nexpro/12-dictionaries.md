# 12. Dictionaries and nested records

[← Previous lesson](11-lists.md) · [Course index](README.md) · [Next lesson →](13-functions.md)

A dictionary stores values under keys.

## Types and syntax

| Type | Syntax | Definition |
|---|---|---|
| Literal | `{"sku": "A-01"}` | Creates an entry with a named key. |
| Update | `item["stock"] = 4` | Adds or replaces an entry. |
| Keys | `keys(item)` | Returns a list of keys in insertion order. |
| Get | `get(item, "stock", 0)` | Returns the value or the fallback if the key is absent. |
| Nested values | `item["counts"][0]` | Accesses a value within a nested list or dictionary. |

## When and why to use it

Keep a product SKU, current stock, and stock history together in one record.

**Advantages.** Meaningful keys are easier to read than positional indexes for named fields.

**Limitations and common mistakes.** Directly reading a missing key raises an error. Assigning the same key again replaces its value.

Use a [structured record](../docs/language.md#structured-records) if the fields must stay fixed.

## Try it

Paste this code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**. [Download the example .pa file](examples/12-dictionaries.pa)

```text
item = {"sku": "A-01", "counts": [2, 4]}
item["counts"][0] = 3
say item["sku"]
say item["counts"][0]
say len(keys(item))
say get(item, "minimum", 0)
```

**Expected result**

```text
A-01
3
2
0
```

## Exercise

Add minimum = 5 and run the same get again.

<details>
<summary>Show the answer</summary>

`item["minimum"] = 5` makes the final line print `5`.

</details>

[← Previous lesson](11-lists.md) · [Course index](README.md) · [Next lesson →](13-functions.md)
