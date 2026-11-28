# Booking Revenue Optimizer

Finds the highest-value set of non-overlapping bookings for one resource. [Read the NexPro code](main.pa)

[Open the live form](https://nexpro-playground.vercel.app/projects/booking-optimizer/) to edit the sample and run the NexPro program in your browser.

## Run

Use NexPro 4.9 or later. Save the sample below as `input.json` and run from the repository root.

```sh
nexpro run projects/booking-optimizer/main.pa < input.json
```

## Sample input

```json
[
  {
    "id": "Full block",
    "start": 0,
    "finish": 6,
    "value_cents": 7000
  },
  {
    "id": "Morning",
    "start": 0,
    "finish": 3,
    "value_cents": 4500
  },
  {
    "id": "Afternoon",
    "start": 3,
    "finish": 6,
    "value_cents": 4500
  },
  {
    "id": "Evening",
    "start": 6,
    "finish": 8,
    "value_cents": 2000
  }
]
```

## Expected output

```json
{
  "accepted": [
    "Morning",
    "Afternoon",
    "Evening"
  ],
  "value_cents": 11000,
  "requests": 4
}
```

The optimizer uses weighted interval scheduling. Time is expressed in whole units. A booking can start exactly when the previous one finishes. Equal-value alternatives keep the earlier solution in finish-time order.
