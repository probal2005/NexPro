# 20. CSV uploads and named downloads

[← Previous lesson](19-validation.md) · [Course index](README.md) · [Next lesson →](21-sharing.md)

A CSV field reads text from a user-selected file. A download call makes output available under a filename.

## Types and syntax

| Type | Syntax | Definition |
|---|---|---|
| Upload | `csv_field(label, columns, default)` | Reads UTF-8 CSV and checks the required columns. |
| Guard | `if file != "" … end` | Skips processing when the file is absent or invalid. |
| Export | `download_csv("stock.csv", text)` | Adds a named download in the browser or writes to standard output in the CLI. |

## When and why to use it

Give users a form where they can choose their own CSV and download a report. Upload a file with the header sku,stock and a single row A-01,4.

**Advantages.** Users can process local files directly in the browser.

**Limitations and common mistakes.** Uploads are limited to 512 KB per file. Combined downloads are limited to 512 KB per run. Missing columns are reported beside the field.

## Try it

Paste this code into the [Playground](https://nexpro-playground.vercel.app/) and select **Preview tool**. [Download the example .pa file](examples/20-csv-tools.pa)

Use the header and just the first data row from [sample-stock.csv](examples/sample-stock.csv) to reproduce the output below. The full file gives two rows.

```text
import "std/csv" as csv
file = csv_field("Stock CSV", ["sku", "stock"])
if file != ""
    rows = csv.parse(file)
    result("Rows", len(rows))
    if len(rows) > 0
        download_csv("stock.csv", csv.stringify(rows))
    end
end
```

**Expected result**

```text
Rows: 1
A Download stock.csv button appears.
```

## Exercise

Remove the stock column and run the tool again.

<details>
<summary>Show the answer</summary>

The field shows `Missing CSV columns: stock`.

</details>

[← Previous lesson](19-validation.md) · [Course index](README.md) · [Next lesson →](21-sharing.md)
