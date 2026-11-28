# 33. CSV and dictionary conversion

[← Previous lesson](32-record-dot-access.md) · [Course index](README.md) · [Next lesson →](34-record-validation.md)

Introduced in NexPro 4.6.

The standard record module converts dictionaries to record instances and exports records as dictionaries.

## Syntax and behavior

- `records.from_dict("Invoice", row)` supplies fields by name.
- `records.to_dict(invoice)` makes a shallow dictionary copy.
- Use `int(row["amount_cents"])` before construction when a CSV cell represents whole cents.

## When to use it

Import typed invoices and export valid rows as JSON.

Conversion applies required fields, defaults, and types. Unknown fields are rejected. The dictionary copy shares nested values with the original.

## Try it

Paste the code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**, or run the [.pa example](../examples/csv_invoice_records.pa) with `nexpro run`.

```text
import "std/csv" as csv
import "std/json" as json
import "std/record" as records

record Invoice(number: string, amount_cents: integer, paid: boolean = false)

invoices = []
row_number = 1
for row in csv.parse("number,amount_cents\nINV-001,1800\nINV-002,invalid\nINV-003,1200")
    row_number = row_number + 1
    try
        row["amount_cents"] = int(row["amount_cents"])
        invoice = records.from_dict("Invoice", row)
        append(invoices, records.to_dict(invoice))
    catch (error)
        say "Skipped row " + json.stringify(row_number) + ": " + error["code"]
    end
end
say json.stringify(invoices)
```

**Expected output**

```text
Skipped row 3: invalid_integer
[{"number": "INV-001", "amount_cents": 1800, "paid": false}, {"number": "INV-003", "amount_cents": 1200, "paid": false}]
```

## Exercise

Change the invalid amount in row 3 to 2500.

<details>
<summary>Show the answer</summary>

The export contains three invoices and no row is skipped.

</details>

[← Previous lesson](32-record-dot-access.md) · [Course index](README.md) · [Next lesson →](34-record-validation.md)
