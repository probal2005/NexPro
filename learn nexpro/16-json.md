# 16. std/json — reading and writing JSON

[← Previous lesson](15-math.md) · [Course index](README.md) · [Next lesson →](17-csv.md)

JSON is a text format for exchanging structured data.

## Types and syntax

| Type | Syntax | Definition |
|---|---|---|
| Parse | `json.parse(text)` | Reads JSON text into a NexPro value. |
| Stringify | `json.stringify(value)` | Turns a NexPro value into JSON text. |

## When and why to use it

Exchange reports or structured input with another program.

**Advantages.** JSON can preserve nested data and Unicode text.

**Limitations and common mistakes.** Malformed JSON and non-finite numbers raise errors. JSON requires double quotes around strings and object keys.

## Try it

Paste this code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**. [Download the example .pa file](examples/16-json.pa)

```text
import "std/json" as json
record = json.parse('{"name": "Ada", "score": 85}')
say record["name"]
say json.stringify([record["score"], 90])
```

**Expected result**

```text
Ada
[85, 90]
```

## Exercise

Change the score to 90 and print the record as JSON.

<details>
<summary>Show the answer</summary>

Write `record["score"] = 90` and then `say json.stringify(record)`.

</details>

[← Previous lesson](15-math.md) · [Course index](README.md) · [Next lesson →](17-csv.md)
