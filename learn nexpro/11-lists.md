# 11. Lists, indexing, and slicing

[← Previous lesson](10-strings.md) · [Course index](README.md) · [Next lesson →](12-dictionaries.md)

A list is a mutable, ordered collection. Use it for common array-like tasks.

## Types and syntax

| Type | Syntax | Definition |
|---|---|---|
| Literal | `[10, 20, 30]` | Creates an ordered collection. |
| Index | `items[0]`, `items[-1]` | Reads the first or last item. |
| Slice | `items[start:stop:step]` | Selects a range with an exclusive stop. |
| Update | `items[0] = 8` | Replaces an item. |
| Append | `append(items, 40)` | Adds to the end of the existing list. |
| Range | `range(1, 6, 2)` | Builds the integer list [1, 3, 5]. |
| Sort and reverse | `sorted(items)`, `reverse(items)` | Return new lists in a different order. |
| Numeric summaries | `sum(items)`, `min(items)`, `max(items)` | Compute a total, smallest value, or largest value. |

## When and why to use it

Store scores, order lines, or records read from a CSV file.

**Advantages.** Indexing, slicing, and loops let you read and process an ordered set.

**Limitations and common mistakes.** An out-of-range index raises an error. Min and max require a non-empty list. Version 3.6 has no dedicated fixed array or linked list.

## Try it

Paste this code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**. [Download the example .pa file](examples/11-lists.pa)

```text
scores = [70, 85, 100]
scores[0] = 75
append(scores, 80)
say scores[-1]
say scores[0:2]
say sorted(scores)
say reverse(range(1, 4))
say sum(scores)
say min(scores)
say max(scores)
```

**Expected result**

```text
80
[75, 85]
[75, 80, 85, 100]
[3, 2, 1]
340
75
100
```

## Exercise

Read the last two scores.

<details>
<summary>Show the answer</summary>

`scores[-2:]` gives `[100, 80]`.

</details>

[← Previous lesson](10-strings.md) · [Course index](README.md) · [Next lesson →](12-dictionaries.md)
