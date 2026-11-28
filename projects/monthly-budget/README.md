# Monthly Budget Checker

Shows remaining or overspent amounts by category and overall. [Read the NexPro code](main.pa)

## Run

From the repository root, pass the sample JSON on standard input.

```sh
printf '%s\n' '[{"category":"Food","budget_cents":20000,"spent_cents":23000},{"category":"Travel","budget_cents":10000,"spent_cents":6500}]' | nexpro run projects/monthly-budget/main.pa
```

To run in the [NexPro Playground](https://nexpro-playground.vercel.app/), copy
`main.pa` into the editor and paste the sample JSON into **Program input**.

## Sample input

```json
[{"category":"Food","budget_cents":20000,"spent_cents":23000},{"category":"Travel","budget_cents":10000,"spent_cents":6500}]
```

## Expected output

```json
{
  "categories": [
    {
      "category": "Food",
      "remaining_cents": -3000,
      "over_budget": true
    },
    {
      "category": "Travel",
      "remaining_cents": 3500,
      "over_budget": false
    }
  ],
  "total_remaining_cents": 500
}
```

Enter budgets and actual spending in integer cents. A negative remaining amount indicates overspending.
