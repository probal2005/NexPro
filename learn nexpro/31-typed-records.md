# 31. Typed record fields

[← Previous lesson](30-records.md) · [Course index](README.md) · [Next lesson →](32-record-dot-access.md)

Introduced in NexPro 4.4.

A field annotation checks the type of a value at construction and reassignment.

## Syntax and behavior

- `amount_cents: integer` accepts an integer.
- `paid: boolean = false` checks a field with a default.
- A type mismatch raises `record_field_type` and includes field, expected, and actual in `error["details"]`.

## When to use it

Prevent amounts read as CSV text from being used as integers by accident.

A failed reassignment preserves the previous value. A type annotation does not convert values or inspect elements inside a list.

## Try it

Paste the code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**, or run the [.pa example](../examples/typed_invoice.pa) with `nexpro run`.

```text
record Invoice(number: string, amount_cents: integer, paid: boolean = false)

invoice = Invoice("INV-001", 1800)
try
    invoice["amount_cents"] = "1800"
catch (error)
    say error["code"]
    say error["details"]["field"]
end
say invoice["amount_cents"]
invoice["paid"] = true
say invoice["paid"]
```

**Expected output**

```text
record_field_type
amount_cents
1800
true
```

## Exercise

Replace the string assignment with the integer 2000.

<details>
<summary>Show the answer</summary>

The reassignment succeeds and the example prints 2000 followed by true.

</details>

[← Previous lesson](30-records.md) · [Course index](README.md) · [Next lesson →](32-record-dot-access.md)
