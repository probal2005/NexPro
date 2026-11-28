# Invoice Audit

Reports invalid invoices by error code and totals the valid amounts. [Read the NexPro code](main.pa)

[Open the live form](https://nexpro-playground.vercel.app/projects/invoice-audit/) to edit the sample and run the program in your browser.

**NexPro features.** Nested typed records, rule validation, and structured field paths.

## Run

Use NexPro 4.9 or later. From the repository root, run the following command.

```sh
printf '%s\n' '[{"number":"I-01","cents":1800,"customer":{"name":"Ada","email":"ada@example.com"}},{"number":"I-02","cents":900,"customer":{"name":"Grace","email":""}},{"number":"I-03","cents":-500,"customer":{"name":"Linus","email":"linus@example.com"}}]' | nexpro run projects/invoice-audit/main.pa
```

You can also select **Invoice Audit** under **Examples → NexPro projects** in the
[Playground](https://nexpro-playground.vercel.app/).

## Sample input

```json
[
  {
    "number": "I-01",
    "cents": 1800,
    "customer": {
      "name": "Ada",
      "email": "ada@example.com"
    }
  },
  {
    "number": "I-02",
    "cents": 900,
    "customer": {
      "name": "Grace",
      "email": ""
    }
  },
  {
    "number": "I-03",
    "cents": -500,
    "customer": {
      "name": "Linus",
      "email": "linus@example.com"
    }
  }
]
```

## Expected output

```json
{
  "valid": [
    {
      "number": "I-01",
      "cents": 1800,
      "customer": {
        "name": "Ada",
        "email": "ada@example.com"
      }
    }
  ],
  "total_cents": 1800,
  "issues": [
    {
      "invoice": "I-02",
      "code": "record_rule",
      "details": {
        "record": "Customer",
        "rule": "email_required",
        "path": "customer"
      }
    },
    {
      "invoice": "I-03",
      "code": "record_rule",
      "details": {
        "record": "Invoice",
        "rule": "amount_nonnegative"
      }
    }
  ]
}
```

An empty email reports the customer rule. In the CLI sample, replacing the empty string with an integer reports the nested path customer.email.
