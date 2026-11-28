# 25. Null, defaults, and elif

[← Previous lesson](24-collection-modules.md) · [Course index](README.md) · [Next lesson →](26-error-recovery.md)

Introduced in NexPro 3.8.

Use null for missing values, defaults for optional parameters, and elif for ordered decisions.

## Syntax and behavior

- `null` is false in a condition and represents JSON null.
- `type_of(value)` returns a type name as text.
- `discount = 0` supplies a default when the caller omits that argument.
- `elif` adds a branch that runs only if earlier conditions failed.

## When to use it

Handle optional discounts or settings without forcing every caller to supply them.

Defaults make common calls shorter. Required parameters must come first. Explicit null is a supplied value, so it does not trigger a default.

## Try it

Paste the code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**, or run the [.pa example](../examples/invoice_total.pa) with `nexpro run`.

```text
import "std/json" as json

function invoice_total(unit_cents, quantity, discount = 0)
    assert unit_cents >= 0 and quantity >= 0
    assert discount >= 0 and discount <= 100
    gross = unit_cents * quantity
    return gross * (100 - discount) // 100
end

say invoice_total(1000, 2)
say invoice_total(1000, 2, 10)

discount = json.parse("null")
if discount == null
    say "No discount supplied"
elif type_of(discount) == "integer"
    say invoice_total(1000, 2, discount)
else
    say "Invalid discount"
end
```

**Expected output**

```text
2000
1800
No discount supplied
```

## Exercise

Change `json.parse("null")` to `25`.

<details>
<summary>Show the answer</summary>

The final branch calculates 1500 cents.

</details>

[← Previous lesson](24-collection-modules.md) · [Course index](README.md) · [Next lesson →](26-error-recovery.md)
