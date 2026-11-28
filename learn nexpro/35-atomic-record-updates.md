# 35. Atomic record updates

[← Previous lesson](34-record-validation.md) · [Course index](README.md) · [Next lesson →](36-nested-records.md)

Introduced in NexPro 4.8.

An atomic update applies several field changes together after validating the entire proposed record.

## Syntax and behavior

- `records.update(invoice, changes)` takes the existing record and a dictionary of changes.
- Field names and types are checked before the record's rules.
- The operation returns the updated record on success.

## When to use it

Update a subtotal and its discount together when changing either in isolation could violate a rule.

A failed update leaves every proposed field unchanged. Update affects the supplied record in place.

## Try it

Paste the code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**, or run the [.pa example](../examples/atomic_invoice.pa) with `nexpro run`.

```text
import "std/record" as records

record Invoice(subtotal: integer, discount: integer)
where "discount_bounds", discount >= 0 and discount <= subtotal, "Discount must be between zero and the subtotal"

invoice = Invoice(1000, 500)
records.update(invoice, {"subtotal": 400, "discount": 100})
say invoice.subtotal - invoice.discount

try
    records.update(invoice, {"subtotal": 300, "discount": 500})
catch (error)
    say error["details"]["rule"]
end
say invoice.subtotal
say invoice.discount
```

**Expected output**

```text
300
discount_bounds
400
100
```

## Exercise

In the failing update, change the proposed discount to 50.

<details>
<summary>Show the answer</summary>

The second update succeeds. The final subtotal and discount are 300 and 50.

</details>

[← Previous lesson](34-record-validation.md) · [Course index](README.md) · [Next lesson →](36-nested-records.md)
