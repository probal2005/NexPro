# Multi-Warehouse Fulfillment Planner

Splits orders across warehouses, prioritizes rush orders, and commits stock deductions only after an entire order can be filled. [Read the NexPro code](main.pa)

All executable project code is written in NexPro. Use NexPro 4.9 or later.

## Run it

[Open the live form](https://nexpro-playground.vercel.app/projects/fulfillment-planner/) to edit inventory, orders, and individual order lines.

In the [NexPro Playground](https://nexpro-playground.vercel.app/), select
**Examples → NexPro projects → Multi-Warehouse Fulfillment Planner**. The editor
loads the entry point and its module, and **Inputs & files** contains the
sample. Select **Run code**.

For the CLI, save the sample to `orders.json` and run this from the repository root.

```sh
nexpro run projects/fulfillment-planner/main.pa < orders.json
nexpro run projects/fulfillment-planner/test_planner.pa
```

## How it works

- [`main.pa`](main.pa) reads JSON and prints a plan or a structured input error.
- [`planner.pa`](planner.pa) indexes stock by SKU, validates typed records,
  combines repeated SKU lines, and uses two FIFO queues to process rush
  orders before standard orders.
- Each order stages deductions by warehouse. If any SKU falls short, the
  planner discards every staged deduction for that order and reports its
  first shortage. The next order can use that stock.
- [`test_planner.pa`](test_planner.pa) checks split allocations, priority
  order, rollback, duplicate IDs and stock entries, and inventory reset
  between runs.

Quantities are whole units. Warehouse order follows the input inventory list,
so the result is deterministic. Repeated warehouse and SKU pairs invalidate
the inventory. Invalid orders are reported by their original row number.
Each run starts from the supplied inventory snapshot.

## Sample input

```json
{
  "inventory": [
    {
      "warehouse": "East",
      "sku": "KIT",
      "available": 2
    },
    {
      "warehouse": "West",
      "sku": "KIT",
      "available": 3
    },
    {
      "warehouse": "West",
      "sku": "CASE",
      "available": 1
    }
  ],
  "orders": [
    {
      "id": "ORD-1",
      "lines": [
        {
          "sku": "KIT",
          "quantity": 1
        }
      ]
    },
    {
      "id": "ORD-2",
      "priority": "rush",
      "lines": [
        {
          "sku": "KIT",
          "quantity": 4
        }
      ]
    },
    {
      "id": "ORD-3",
      "priority": "rush",
      "lines": [
        {
          "sku": "KIT",
          "quantity": 1
        },
        {
          "sku": "CASE",
          "quantity": 2
        }
      ]
    },
    {
      "id": "ORD-4",
      "lines": []
    }
  ]
}
```

## Expected output

```json
{
  "orders": [
    {
      "id": "ORD-2",
      "status": "fulfilled",
      "allocations": [
        {
          "warehouse": "East",
          "sku": "KIT",
          "quantity": 2
        },
        {
          "warehouse": "West",
          "sku": "KIT",
          "quantity": 2
        }
      ],
      "units": 4
    },
    {
      "id": "ORD-3",
      "status": "backordered",
      "shortage": {
        "sku": "CASE",
        "quantity": 1
      },
      "allocations": [],
      "units": 0
    },
    {
      "id": "ORD-1",
      "status": "fulfilled",
      "allocations": [
        {
          "warehouse": "West",
          "sku": "KIT",
          "quantity": 1
        }
      ],
      "units": 1
    }
  ],
  "invalid_orders": [
    {
      "row": 4,
      "code": "empty_order",
      "message": "An order must have at least one line"
    }
  ],
  "remaining_inventory": [
    {
      "warehouse": "East",
      "sku": "KIT",
      "available": 0
    },
    {
      "warehouse": "West",
      "sku": "KIT",
      "available": 0
    },
    {
      "warehouse": "West",
      "sku": "CASE",
      "available": 1
    }
  ],
  "summary": {
    "fulfilled": 2,
    "backordered": 1,
    "invalid": 1,
    "allocated_units": 5
  }
}
```

Even though `ORD-1` appears first, rush order `ORD-2` takes two KITs from each
warehouse. `ORD-3` is one CASE short, so it keeps none of its tentative stock.
`ORD-1` can then claim the final KIT.
