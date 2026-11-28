# 36. Nested records and error paths

[← Previous lesson](35-atomic-record-updates.md) · [Course index](README.md)

Introduced in NexPro 4.9.

A nested field annotation names another record type, such as customer: Customer.

## Syntax and behavior

- `record Invoice(number: string, customer: Customer)` requires the declared Customer type.
- `records.from_dict()` converts child dictionaries through their declared constructors.
- `error["details"]["path"]` identifies a nested failure, such as `customer.email`.

## When to use it

Import an invoice and its customer together while applying the customer's own defaults and rules.

Nested errors identify the affected field. Direct assignment requires an instance of the declared type. Updating a nested record runs that record's own rules.

## Try it

Paste the code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**, or run the [.pa example](../examples/nested_invoice.pa) with `nexpro run`.

```text
import "std/json" as json
import "std/record" as records

record Customer(email: string, active: boolean = true)
where "email_required", email != "", "Email is required"

record Invoice(number: string, customer: Customer)

invoice = records.from_dict("Invoice", {"number": "INV-001", "customer": {"email": "ada@example.com"}})
say invoice.customer.active
say json.stringify(invoice)

try
    records.from_dict("Invoice", {"number": "INV-002", "customer": {"email": 25}})
catch (error)
    say error["details"]["path"]
    say error["message"]
end
```

**Expected output**

```text
true
{"number": "INV-001", "customer": {"email": "ada@example.com", "active": true}}
customer.email
Field 'email' of record 'Customer' expects string, got integer
```

## Exercise

In the failing import, change the email value from 25 to an empty string.

<details>
<summary>Show the answer</summary>

The type check passes but the email rule fails. The path is customer and the rule is email_required.

</details>

[← Previous lesson](35-atomic-record-updates.md) · [Course index](README.md)
