# Subscription Change Simulator

Applies changes to seats, price, and credit as a single validated update. [Read the NexPro code](main.pa)

[Open the live form](https://nexpro-playground.vercel.app/projects/subscription-changes/) to edit the sample and run the program in your browser.

**NexPro features.** Typed records, cross-field rules, and atomic updates.

## Run

Use NexPro 4.9 or later. From the repository root, run the following command.

```sh
printf '%s\n' '{"plan":{"seats":4,"unit_cents":1000,"credit_cents":3500},"changes":[{"seats":2,"unit_cents":1000,"credit_cents":1000},{"seats":1,"unit_cents":1000,"credit_cents":2000}]}' | nexpro run projects/subscription-changes/main.pa
```

You can also select **Subscription Change Simulator** under **Examples → NexPro projects** in the
[Playground](https://nexpro-playground.vercel.app/).

## Sample input

```json
{
  "plan": {
    "seats": 4,
    "unit_cents": 1000,
    "credit_cents": 3500
  },
  "changes": [
    {
      "seats": 2,
      "unit_cents": 1000,
      "credit_cents": 1000
    },
    {
      "seats": 1,
      "unit_cents": 1000,
      "credit_cents": 2000
    }
  ]
}
```

## Expected output

```json
{
  "history": [
    {
      "accepted": true,
      "plan": {
        "seats": 2,
        "unit_cents": 1000,
        "credit_cents": 1000
      }
    },
    {
      "accepted": false,
      "code": "record_rule",
      "plan": {
        "seats": 2,
        "unit_cents": 1000,
        "credit_cents": 1000
      }
    }
  ],
  "due_cents": 1000
}
```

The first change reduces the seat count and credit together. The second change fails and preserves the accepted plan.
