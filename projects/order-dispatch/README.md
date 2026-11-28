# Order Dispatch Checker

Separates ready orders from orders that need attention. [Read the NexPro code](main.pa)

## Run

From the repository root, pass the sample JSON on standard input.

```sh
printf '%s\n' '[{"id":"1041","paid":true,"address":"12 Green Street","quantity":2},{"id":"1042","paid":false,"address":" ","quantity":0}]' | nexpro run projects/order-dispatch/main.pa
```

To run in the [NexPro Playground](https://nexpro-playground.vercel.app/), copy
`main.pa` into the editor and paste the sample JSON into **Program input**.

## Sample input

```json
[{"id":"1041","paid":true,"address":"12 Green Street","quantity":2},{"id":"1042","paid":false,"address":" ","quantity":0}]
```

## Expected output

```json
{
  "ready": [
    "1041"
  ],
  "blocked": [
    {
      "id": "1042",
      "reasons": [
        "Payment pending",
        "Missing delivery address",
        "Invalid quantity"
      ]
    }
  ]
}
```

Use a JSON boolean for `paid`, a text address, and a positive whole number for quantity. The report lists every failing rule for each blocked order.
