# Principal Repayment Ledger

Applies principal payments in order and keeps the balance consistent when a payment fails. [Read the NexPro code](main.pa)

[Open the live form](https://nexpro-playground.vercel.app/projects/loan-repayment/) to edit the sample and run the program in your browser.

**NexPro features.** Named arguments, custom errors, and atomic balance changes.

## Run

Use NexPro 4.9 or later. From the repository root, run the following command.

```sh
printf '%s\n' '{"principal_cents":10000,"payments":[{"reference":"Deposit","cents":2500},{"reference":"Overpayment","cents":8000},{"reference":"Second payment","cents":2000}]}' | nexpro run projects/loan-repayment/main.pa
```

You can also select **Principal Repayment Ledger** under **Examples → NexPro projects** in the
[Playground](https://nexpro-playground.vercel.app/).

## Sample input

```json
{
  "principal_cents": 10000,
  "payments": [
    {
      "reference": "Deposit",
      "cents": 2500
    },
    {
      "reference": "Overpayment",
      "cents": 8000
    },
    {
      "reference": "Second payment",
      "cents": 2000
    }
  ]
}
```

## Expected output

```json
{
  "balance": {
    "outstanding_cents": 5500,
    "received_cents": 4500
  },
  "payments": [
    {
      "reference": "Deposit",
      "remaining_cents": 7500
    },
    {
      "reference": "Second payment",
      "remaining_cents": 5500
    }
  ],
  "issues": [
    {
      "reference": "Overpayment",
      "message": "A payment cannot exceed the outstanding balance"
    }
  ]
}
```

This ledger tracks principal only. It does not calculate interest or fees.
