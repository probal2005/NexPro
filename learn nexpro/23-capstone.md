# 23. Capstone — inventory reorder tool

[← Previous lesson](22-cli-debug-test.md) · [Course index](README.md)

Build a complete workflow that reads stock records, applies a reorder rule, and exports the result.

## Types and syntax

| Type | Syntax | Definition |
|---|---|---|
| Input | `csv_field()` | Reads a table of product codes and stock levels. |
| Rule | `if stock <= minimum` | Checks which items need to be reordered. |
| Collection | List of dictionaries | Holds the output rows. |
| Export | `csv.stringify()` and `download_csv()` | Creates a named report. |

## When and why to use it

Upload sample-stock.csv in Preview tool and select Calculate. Compare the result with the full Inventory Reorder example.

**Advantages.** The project combines form inputs, validation, loops, collections, and CSV output.

**Limitations and common mistakes.** This short version expects whole numbers. The full Inventory Reorder example reports invalid numbers with their row positions.

## Try it

Paste this code into the [Playground](https://nexpro-playground.vercel.app/) and select **Preview tool**. [Download the example .pa file](examples/23-capstone.pa)

[Sample CSV](examples/sample-stock.csv) · [Full Inventory Reorder source](../examples/tool_inventory.pa) · [Live tool](https://nexpro-playground.vercel.app/tool.html?example=inventory)

```text
import "std/csv" as csv
file = csv_field("Stock CSV", ["sku", "stock", "minimum", "target"])
if file != ""
    orders = []
    for item in csv.parse(file)
        stock = int(item["stock"])
        minimum = int(item["minimum"])
        target = int(item["target"])
        assert stock >= 0 and minimum >= 0 and target > minimum
        if stock <= minimum
            append(orders, {"sku": item["sku"], "quantity": target - stock})
        end
    end
    result("Reorder count", len(orders))
    if len(orders) > 0
        download_csv("reorder.csv", csv.stringify(orders))
    else
        download_csv("reorder.csv", "sku,quantity")
    end
end
```

**Expected result**

```text
Reorder count: 1

reorder.csv:
sku,quantity
A-01,8
```

## Exercise

Change the stock for B-02 from 7 to 2 and run again.

<details>
<summary>Show the answer</summary>

The report now contains two orders. B-02 has a reorder quantity of `9 - 2 = 7`.

</details>

[← Previous lesson](22-cli-debug-test.md) · [Course index](README.md)
