# Inventory Reorder Report

Flags items at or below minimum stock and calculates reorder quantities. [Read the NexPro code](main.pa)

[Open the live form](https://nexpro-playground.vercel.app/projects/inventory-reorder/) to edit the sample and run the NexPro program in your browser.

## Run

From the repository root, pass the sample JSON on standard input.

```sh
printf '%s\n' '[{"sku":"PAPER","stock":3,"minimum":5,"target":15},{"sku":"PEN","stock":20,"minimum":10,"target":30}]' | nexpro run projects/inventory-reorder/main.pa
```

To run in the [NexPro Playground](https://nexpro-playground.vercel.app/), copy
`main.pa` into the editor and paste the sample JSON into **Program input**.

## Sample input

```json
[{"sku":"PAPER","stock":3,"minimum":5,"target":15},{"sku":"PEN","stock":20,"minimum":10,"target":30}]
```

## Expected output

```json
{
  "reorder": [
    {
      "sku": "PAPER",
      "quantity": 12
    }
  ]
}
```

Stock levels are non-negative whole numbers. The target must exceed the minimum.
