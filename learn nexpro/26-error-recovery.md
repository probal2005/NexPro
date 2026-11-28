# 26. Recovering from runtime errors

[← Previous lesson](25-optional-values.md) · [Course index](README.md) · [Next lesson →](27-queues-and-statistics.md)

Introduced in NexPro 3.9.

A try block lets a program recover when an operation raises a runtime error.

## Syntax and behavior

- `try … catch message … end` binds the error message as text.
- `throw "reason"` raises a runtime error explicitly.
- Put the try block inside a loop to handle each row separately.

## When to use it

Continue importing valid rows after a failed numeric conversion.

Recovery keeps unrelated rows moving. Syntax and import errors are reported before execution. Choose a narrow try block so unrelated failures do not get skipped.

## Try it

Paste the code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**, or run the [.pa example](../examples/recover_csv.pa) with `nexpro run`.

```text
import "std/csv" as csv

rows = csv.parse("sku,quantity\nA,4\nB,invalid\nC,-1\nD,6")
total = 0
for row in rows
    try
        quantity = int(row["quantity"])
        if quantity < 0
            throw "Quantity must be nonnegative"
        end
        total = total + quantity
    catch message
        say "Skipped " + row["sku"] + ": " + message
    end
end
say total
```

**Expected output**

```text
Skipped B: invalid literal for int() with base 10: 'invalid'
Skipped C: Quantity must be nonnegative
10
```

## Exercise

Change the final quantity from 6 to 8.

<details>
<summary>Show the answer</summary>

The total is 12. The same two invalid rows are skipped.

</details>

[← Previous lesson](25-optional-values.md) · [Course index](README.md) · [Next lesson →](27-queues-and-statistics.md)
