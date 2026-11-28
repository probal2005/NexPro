# Group Expense Settlement

Equalizes contributions and reports who should pay whom. [Read the NexPro code](main.pa)

[Open the live form](https://nexpro-playground.vercel.app/projects/expense-settlement/) to edit the sample and run the NexPro program in your browser.

## Run

From the repository root, pass the sample JSON on standard input.

```sh
printf '%s\n' '{"participants":[{"name":"Ada","paid_cents":8000},{"name":"Ben","paid_cents":2000},{"name":"Chen","paid_cents":0}]}' | nexpro run projects/expense-settlement/main.pa
```

To run in the [NexPro Playground](https://nexpro-playground.vercel.app/), copy
`main.pa` into the editor and paste the sample JSON into **Program input**.

## Sample input

```json
{"participants":[{"name":"Ada","paid_cents":8000},{"name":"Ben","paid_cents":2000},{"name":"Chen","paid_cents":0}]}
```

## Expected output

```json
{
  "total_cents": 10000,
  "shares": [
    {
      "name": "Ada",
      "share_cents": 3334
    },
    {
      "name": "Ben",
      "share_cents": 3333
    },
    {
      "name": "Chen",
      "share_cents": 3333
    }
  ],
  "payments": [
    {
      "from": "Ben",
      "to": "Ada",
      "cents": 1333
    },
    {
      "from": "Chen",
      "to": "Ada",
      "cents": 3333
    }
  ]
}
```

Names must be unique after trimming. Amounts use non-negative integer cents. The total is capped at 99,999,999,999 cents so division can allocate whole-cent shares accurately. Remainder cents go to the earliest participants. Attach [settlement.pa](settlement.pa) in the Playground, or run `nexpro run projects/expense-settlement/test_settlement.pa` to try the native tests.
