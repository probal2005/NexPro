# 34. Record validation rules

[← Previous lesson](33-record-conversion.md) · [Course index](README.md) · [Next lesson →](35-atomic-record-updates.md)

Introduced in NexPro 4.7.

A where clause enforces a business rule using an expression over the record's fields.

## Syntax and behavior

- `where "nonnegative_amount", amount_cents >= 0, "Amount must be nonnegative"` defines a named rule.
- Constructors, dictionary conversion, and assignment check the rule.
- A failed rule raises `record_rule` with a rule name in `error["details"]["rule"]`.

## When to use it

Reject negative invoice amounts while keeping the rest of a CSV import.

Records enforce the same rule at each write. Rules are evaluated in declaration order and cannot call functions.

## Try it

Paste the code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**, or run the [.pa example](../examples/validated_invoice.pa) with `nexpro run`.

```text
import "std/csv" as csv
import "std/json" as json
import "std/record" as records

record Invoice(number: string, amount_cents: integer, paid: boolean = false)
where "nonnegative_amount", amount_cents >= 0, "Amount must be nonnegative"

invoices = []
row_number = 1
for row in csv.parse("number,amount_cents\nINV-001,1800\nINV-002,-500\nINV-003,1200")
    row_number = row_number + 1
    try
        row["amount_cents"] = int(row["amount_cents"])
        invoice = records.from_dict("Invoice", row)
        append(invoices, records.to_dict(invoice))
    catch (error)
        say "Skipped row " + json.stringify(row_number) + ": " + error["details"]["rule"]
    end
end
say json.stringify(invoices)
```

**Expected output**

```text
Skipped row 3: nonnegative_amount
[{"number": "INV-001", "amount_cents": 1800, "paid": false}, {"number": "INV-003", "amount_cents": 1200, "paid": false}]
```

## Exercise

Replace the negative amount with 0.

<details>
<summary>Show the answer</summary>

The rule accepts zero, so all three invoices are exported.

</details>

[← Previous lesson](33-record-conversion.md) · [Course index](README.md) · [Next lesson →](35-atomic-record-updates.md)
