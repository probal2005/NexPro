# Ledger Reconciliation

Compares a ledger and bank statement by reference, then reports unmatched entries and balance differences. [Read the NexPro code](main.pa)

[Open the live form](https://nexpro-playground.vercel.app/projects/reconciliation/) to edit the sample and run the NexPro program in your browser.

## Run

Use NexPro 4.9 or later. Save the sample below as `input.json` and run from the repository root.

```sh
nexpro run projects/reconciliation/main.pa < input.json
```

## Sample input

```json
{
  "ledger": [
    {
      "reference": "A",
      "cents": 1200
    },
    {
      "reference": "B",
      "cents": -500
    },
    {
      "reference": "C",
      "cents": 200
    }
  ],
  "bank": [
    {
      "reference": "A",
      "cents": 1200
    },
    {
      "reference": "B",
      "cents": -450
    },
    {
      "reference": "D",
      "cents": 300
    }
  ]
}
```

## Expected output

```json
{
  "matched": [
    "A"
  ],
  "mismatches": [
    {
      "reference": "B",
      "ledger_cents": -500,
      "bank_cents": -450,
      "difference_cents": 50
    }
  ],
  "ledger_only": [
    {
      "reference": "C",
      "cents": 200
    }
  ],
  "bank_only": [
    {
      "reference": "D",
      "cents": 300
    }
  ],
  "balance_difference_cents": 150
}
```

Amounts are signed whole cents. A reference may appear once per statement. The reported balance difference is the bank total minus the ledger total.
