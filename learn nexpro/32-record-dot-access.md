# 32. Record dot access

[← Previous lesson](31-typed-records.md) · [Course index](README.md) · [Next lesson →](33-record-conversion.md)

Introduced in NexPro 4.5.

Dot access reads and writes a record field by a name written directly in the code.

## Syntax and behavior

- `invoice.paid = true` updates a field.
- `invoice["paid"]` accesses the same value by key.
- Bracket access also accepts a computed key.

## When to use it

Use dot access for known invoice fields and bracket access for fields selected at runtime.

Both access forms enforce the record's type rules. Module aliases remain available for exports and calls. An alias takes precedence for a matching dotted name.

## Try it

Paste the code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**, or run the [.pa example](../examples/record_fields.pa) with `nexpro run`.

```text
record Invoice(amount_cents: integer, paid: boolean = false)
invoice = Invoice(1800)
invoice.paid = true
say invoice["paid"]
try
    invoice.amount_cents = "1800"
catch (error)
    say error["code"]
end
say invoice.amount_cents
```

**Expected output**

```text
true
record_field_type
1800
```

## Exercise

Change `invoice.paid = true` to bracket assignment.

<details>
<summary>Show the answer</summary>

The output stays identical.

</details>

[← Previous lesson](31-typed-records.md) · [Course index](README.md) · [Next lesson →](33-record-conversion.md)
