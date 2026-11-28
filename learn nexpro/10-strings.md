# 10. Strings, indexing, slicing, and text functions

[← Previous lesson](09-loops.md) · [Course index](README.md) · [Next lesson →](11-lists.md)

A string is a sequence of Unicode characters. NexPro includes five built-in text helpers.

## Types and syntax

| Type | Syntax | Definition |
|---|---|---|
| Trim | `trim("  Ada  ")` | Removes leading and trailing whitespace. |
| Lower | `lower("ADA")` | Converts text to lowercase. |
| Upper | `upper("ada")` | Converts text to uppercase. |
| Split | `split("A,B", ",")` | Splits text into a list at a separator. |
| Join | `join(["A", "B"], "-")` | Combines strings with a separator. |
| Index and slice | `name[0]`, `name[0:2]` | Reads one character or a range of characters. |
| Escape | `"A\nB"` | Includes a newline inside a string. |

## When and why to use it

Clean form input or build a report label from several values.

**Advantages.** The same text operations work with Unicode input.

**Limitations and common mistakes.** Split requires a non-empty separator. Join requires a list of strings. Use std/csv for CSV cells that may contain quoted commas.

## Try it

Paste this code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**. [Download the example .pa file](examples/10-strings.pa)

```text
name = trim("  Ada  ")
say lower(name)
say upper(name)
say name[0:2]
say join(split("A,B", ","), " + ")
say "Nex" + "Pro"
```

**Expected result**

```text
ada
ADA
Ad
A + B
NexPro
```

## Exercise

Turn " red,green " into "RED-GREEN".

<details>
<summary>Show the answer</summary>

`upper(join(split(trim(" red,green "), ","), "-"))`.

</details>

[← Previous lesson](09-loops.md) · [Course index](README.md) · [Next lesson →](11-lists.md)
