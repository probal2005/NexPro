# 18. Forms and input controls

[← Previous lesson](17-csv.md) · [Course index](README.md) · [Next lesson →](19-validation.md)

A .pa program can declare browser form controls and display labeled results.

## Types and syntax

| Type | Syntax | Definition |
|---|---|---|
| Number | `number_field(label, default, min, max, step, message)` | Declares numeric input with optional bounds, a step, and a validation message. |
| Text | `text_field(label, default)` | Declares a text input. |
| Select | `select_field(label, options, default)` | Declares a dropdown. |
| Checkbox | `checkbox_field(label, default)` | Declares a true-or-false control. |
| Result | `result(label, value)` | Displays a labeled value. |

## When and why to use it

Keep quote inputs and arithmetic in one program. Change a field in the generated form and press Calculate.

**Advantages.** The Playground generates a form from the declarations.

**Limitations and common mistakes.** Keep field labels unique. The CLI and compiled Python use default field values and print results to standard output.

## Try it

Paste this code into the [Playground](https://nexpro-playground.vercel.app/) and select **Preview tool**. [Download the example .pa file](examples/18-forms.pa)

```text
client = text_field("Client", "Ada")
hours = number_field("Hours", 4, 1, 20, 1)
currency = select_field("Currency", ["BDT", "USD"], "BDT")
include_fee = checkbox_field("Include service fee", true)
total = hours * 50
if include_fee
    total = total + 25
end
result("Client", client)
result("Currency", currency)
result("Total", total)
```

**Expected result**

```text
Client: Ada
Currency: BDT
Total: 225
```

## Exercise

What is the total when the service fee box is unchecked?

<details>
<summary>Show the answer</summary>

The total is `200`.

</details>

[← Previous lesson](17-csv.md) · [Course index](README.md) · [Next lesson →](19-validation.md)
