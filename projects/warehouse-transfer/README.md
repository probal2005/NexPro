# Warehouse Transfer Simulator

Moves stock between locations while protecting source balance and destination capacity. [Read the NexPro code](main.pa)

[Open the live form](https://nexpro-playground.vercel.app/projects/warehouse-transfer/) to edit the sample and run the program in your browser.

**NexPro features.** Cross-field record rules and atomic updates.

## Run

Use NexPro 4.9 or later. From the repository root, run the following command.

```sh
printf '%s\n' '{"stock":{"source":12,"destination":3,"destination_capacity":10},"quantities":[5,4,2]}' | nexpro run projects/warehouse-transfer/main.pa
```

You can also select **Warehouse Transfer Simulator** under **Examples → NexPro projects** in the
[Playground](https://nexpro-playground.vercel.app/).

## Sample input

```json
{
  "stock": {
    "source": 12,
    "destination": 3,
    "destination_capacity": 10
  },
  "quantities": [
    5,
    4,
    2
  ]
}
```

## Expected output

```json
{
  "stock": {
    "source": 5,
    "destination": 10,
    "destination_capacity": 10
  },
  "history": [
    {
      "quantity": 5,
      "accepted": true
    },
    {
      "quantity": 4,
      "accepted": false,
      "message": "Stock must fit both locations"
    },
    {
      "quantity": 2,
      "accepted": true
    }
  ]
}
```

A rejected transfer changes neither stock level.
