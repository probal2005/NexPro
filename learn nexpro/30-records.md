# 30. Structured records

[← Previous lesson](29-named-arguments.md) · [Course index](README.md) · [Next lesson →](31-typed-records.md)

Introduced in NexPro 4.3.

A record declaration defines the fields, required values, and defaults for a reusable data shape.

## Syntax and behavior

- `record Invoice(number, amount_cents, paid = false)` declares the shape.
- `Invoice(number = "INV-001", amount_cents = 1800)` constructs an instance.
- `invoice["paid"]` reads or writes a declared field.

## When to use it

Store invoice data with predictable fields across an application.

Constructors check required fields. The shape stays fixed, but existing fields can change. JSON exports record fields as an object and parses the object back as a dictionary.

## Try it

Paste the code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**, or run the [.pa example](../examples/invoice_record.pa) with `nexpro run`.

```text
import "std/json" as json

record Invoice(number, amount_cents, currency = "USD", paid = false)

invoice = Invoice(number = "INV-001", amount_cents = 1800)
invoice["paid"] = true
say type_of(invoice)
say invoice["currency"]
say json.stringify(invoice)

try
    invoice["unknown"] = 1
catch (error)
    say error["code"]
end
```

**Expected output**

```text
record
USD
{"number": "INV-001", "amount_cents": 1800, "currency": "USD", "paid": true}
missing_key
```

## Exercise

Remove the amount from the constructor call.

<details>
<summary>Show the answer</summary>

Construction fails because amount_cents is required.

</details>

[← Previous lesson](29-named-arguments.md) · [Course index](README.md) · [Next lesson →](31-typed-records.md)
