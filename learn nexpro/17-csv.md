# 17. std/csv — reading and writing tables

[← Previous lesson](16-json.md) · [Course index](README.md) · [Next lesson →](18-forms.md)

The first CSV row contains column names. Each data row becomes a dictionary.

## Types and syntax

| Type | Syntax | Definition |
|---|---|---|
| Parse | `csv.parse(text)` | Reads CSV cells as strings. |
| Required columns | `csv.parse(text, ["sku", "stock"])` | Checks that the listed headers are present. |
| Stringify | `csv.stringify(rows)` | Writes a list of dictionaries with matching columns as CSV. |

## When and why to use it

Read spreadsheet exports, inventory lists, and reports.

**Advantages.** The parser handles quoted commas and multiline cells.

**Limitations and common mistakes.** Convert cell text before doing numeric calculations. Duplicate headers and incorrect column counts produce errors.

## Try it

Paste this code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**. [Download the example .pa file](examples/17-csv.pa)

```text
import "std/csv" as csv
rows = csv.parse('sku,stock
"A, large",4', ["sku", "stock"])
say rows[0]["sku"]
say int(rows[0]["stock"]) + 2
say csv.stringify([{"sku": "A-01", "quantity": 2}])
```

**Expected result**

```text
A, large
6
sku,quantity
A-01,2
```

## Exercise

Remove stock from the header but keep it in the required list.

<details>
<summary>Show the answer</summary>

The parser reports `Missing CSV columns: stock`.

</details>

[← Previous lesson](16-json.md) · [Course index](README.md) · [Next lesson →](18-forms.md)
