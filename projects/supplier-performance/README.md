# Supplier Delivery Performance

Summarizes deliveries, on-time counts, and median delay by supplier. [Read the NexPro code](main.pa)

[Open the live form](https://nexpro-playground.vercel.app/projects/supplier-performance/) to edit the sample and run the program in your browser.

**NexPro features.** Typed delivery records, structured catches, and std/stats.

## Run

Use NexPro 4.9 or later. From the repository root, run the following command.

```sh
printf '%s\n' '[{"supplier":"North","planned_days":5,"actual_days":4},{"supplier":"North","planned_days":5,"actual_days":8},{"supplier":"South","planned_days":3,"actual_days":3},{"supplier":"South","planned_days":-1,"actual_days":3}]' | nexpro run projects/supplier-performance/main.pa
```

You can also select **Supplier Delivery Performance** under **Examples → NexPro projects** in the
[Playground](https://nexpro-playground.vercel.app/).

## Sample input

```json
[
  {
    "supplier": "North",
    "planned_days": 5,
    "actual_days": 4
  },
  {
    "supplier": "North",
    "planned_days": 5,
    "actual_days": 8
  },
  {
    "supplier": "South",
    "planned_days": 3,
    "actual_days": 3
  },
  {
    "supplier": "South",
    "planned_days": -1,
    "actual_days": 3
  }
]
```

## Expected output

```json
{
  "suppliers": [
    {
      "supplier": "North",
      "deliveries": 2,
      "on_time": 1,
      "median_delay": 1
    },
    {
      "supplier": "South",
      "deliveries": 1,
      "on_time": 1,
      "median_delay": 0
    }
  ],
  "issues": [
    {
      "supplier": "South",
      "message": "Delivery days cannot be negative"
    }
  ]
}
```

Delay is the actual time minus the planned time. Negative delays indicate early delivery.
