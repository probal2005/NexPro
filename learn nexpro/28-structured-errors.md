# 28. Structured errors and custom codes

[← Previous lesson](27-queues-and-statistics.md) · [Course index](README.md) · [Next lesson →](29-named-arguments.md)

Introduced in NexPro 4.1.

Structured catches expose an error as a dictionary so decisions can use a stable code.

## Syntax and behavior

- `catch (error)` provides `code`, `message`, `file`, `line`, and `function`.
- `catch message` receives only text.
- `throw "code", "message"` raises a custom code.

## When to use it

Stop a CSV import if the header is missing, while skipping individual rows with invalid quantities.

Programs can branch on codes such as `csv_missing_columns` and `invalid_integer`. Error location fields can be null and optional details vary by error.

## Try it

Paste the code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**, or run the [.pa example](../examples/structured_inventory.pa) with `nexpro run`.

```text
import "std/csv" as csv
import "std/json" as json

function import_inventory(text)
    try
        rows = csv.parse(text, ["sku", "quantity"])
    catch (error)
        if error["code"] == "csv_missing_columns"
            say "Stopped: " + error["code"]
            return null
        end
        throw error["code"], error["message"]
    end

    total = 0
    row_number = 1
    for row in rows
        row_number = row_number + 1
        try
            quantity = int(row["quantity"])
            if quantity < 0
                throw "invalid_integer", "Quantity cannot be negative"
            end
            total = total + quantity
        catch (error)
            if error["code"] != "invalid_integer"
                throw error["code"], error["message"]
            end
            say "Skipped row " + json.stringify(row_number) + ": " + error["code"]
        end
    end
    return total
end

say import_inventory("sku,quantity\nA,4\nB,invalid\nC,6")
import_inventory("sku\nA")
```

**Expected output**

```text
Skipped row 3: invalid_integer
10
Stopped: csv_missing_columns
```

## Exercise

Change the invalid quantity to 2.

<details>
<summary>Show the answer</summary>

The first import totals 12. The separate example with a missing column still stops.

</details>

[← Previous lesson](27-queues-and-statistics.md) · [Course index](README.md) · [Next lesson →](29-named-arguments.md)
