# 29. Named arguments

[← Previous lesson](28-structured-errors.md) · [Course index](README.md) · [Next lesson →](30-records.md)

Introduced in NexPro 4.2.

A named argument fills a particular parameter by name.

## Syntax and behavior

- `invoice_total(1000, 2, discount = 10)` mixes positional and named arguments.
- `invoice_total(unit_cents = 1000)` names a required parameter and uses defaults for the others.

## When to use it

Set a discount or shipping fee without filling every optional parameter.

Names make long calls easier to read. Positional arguments must come first. Unknown or duplicate arguments raise errors. Built-in and standard-library functions use positional arguments.

## Try it

Paste the code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**, or run the [.pa example](../examples/named_invoice.pa) with `nexpro run`.

```text
function invoice_total(unit_cents, quantity = 1, shipping_cents = 0, discount = 0)
    subtotal = unit_cents * quantity * (100 - discount) // 100
    return subtotal + shipping_cents
end

say invoice_total(1000, 2, discount = 10)
say invoice_total(unit_cents = 1000, shipping_cents = 250)
```

**Expected output**

```text
1800
1250
```

## Exercise

Call the function with 1000 cents, quantity 2, and shipping 250 cents.

<details>
<summary>Show the answer</summary>

`invoice_total(1000, 2, shipping_cents = 250)` returns 2250.

</details>

[← Previous lesson](28-structured-errors.md) · [Course index](README.md) · [Next lesson →](30-records.md)
