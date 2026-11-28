# Expense Policy Review

Applies spending limits to expenses and reports approved totals and flagged entries. [Read the NexPro code](main.pa)

[Open the live form](https://nexpro-playground.vercel.app/projects/expense-policy/) to edit the sample and run the program in your browser.

**NexPro features.** Named arguments, default limits, typed records, and rule errors.

## Run

Use NexPro 4.9 or later. From the repository root, run the following command.

```sh
printf '%s\n' '{"meal_cap":2000,"expenses":[{"id":"E-01","category":"meal","cents":1800},{"id":"E-02","category":"meal","cents":2500},{"id":"E-03","category":"travel","cents":9000},{"id":"E-04","category":"travel","cents":-50}]}' | nexpro run projects/expense-policy/main.pa
```

You can also select **Expense Policy Review** under **Examples → NexPro projects** in the
[Playground](https://nexpro-playground.vercel.app/).

## Sample input

```json
{
  "meal_cap": 2000,
  "expenses": [
    {
      "id": "E-01",
      "category": "meal",
      "cents": 1800
    },
    {
      "id": "E-02",
      "category": "meal",
      "cents": 2500
    },
    {
      "id": "E-03",
      "category": "travel",
      "cents": 9000
    },
    {
      "id": "E-04",
      "category": "travel",
      "cents": -50
    }
  ]
}
```

## Expected output

```json
{
  "approved_cents": 10800,
  "decisions": [
    {
      "id": "E-01",
      "status": "approved"
    },
    {
      "id": "E-02",
      "status": "review"
    },
    {
      "id": "E-03",
      "status": "approved"
    },
    {
      "id": "E-04",
      "status": "invalid",
      "code": "record_rule"
    }
  ]
}
```

Amounts are whole cents. The general limit defaults to 10,000 cents.
