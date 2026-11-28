# 19. Validation, assertions, and runtime errors

[← Previous lesson](18-forms.md) · [Course index](README.md) · [Next lesson →](20-csv-tools.md)

Validation explains how to correct input. An assertion checks a condition the program requires.

## Types and syntax

| Type | Syntax | Definition |
|---|---|---|
| Assertion | `assert quantity >= 0` | Raises a runtime error if the condition is false. |
| Field validation | `field_check(label, condition, message)` | Displays a message beside the declared field in the browser. |
| Numeric bounds | `number_field("Quantity", 2, 1, 20, 1)` | Accepts whole numbers from 1 to 20. |
| Stack trace | Source file and line from a runtime error | Identifies a failed operation and the calls that reached it. |

## When and why to use it

Tell users how to correct an empty name, negative quantity, or out-of-range value before relying on the result.

**Advantages.** Invalid data can be caught close to where it enters the program.

**Limitations and common mistakes.** A failed field_check raises an error in the terminal. Version 3.6 has no try/catch syntax.

## Try it

Paste this code into the [Playground](https://nexpro-playground.vercel.app/) and select **Preview tool**. [Download the example .pa file](examples/19-validation.pa)

```text
name = text_field("Name", "Ada")
quantity = number_field("Quantity", 2, 1, 20, 1)
assert quantity > 0
if field_check("Name", len(trim(name)) > 0, "Enter a name.")
    result("Order", name)
end
```

**Expected result**

```text
Order: Ada
```

## Exercise

Clear Name and press Calculate.

<details>
<summary>Show the answer</summary>

The Name field shows `Enter a name.`.

</details>

[← Previous lesson](18-forms.md) · [Course index](README.md) · [Next lesson →](20-csv-tools.md)
