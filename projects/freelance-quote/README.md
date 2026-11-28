# Freelance Quote Generator

Converts hours, rates, and a discount into an itemized quote. [Read the NexPro code](main.pa)

[Open the live form](https://nexpro-playground.vercel.app/projects/freelance-quote/) to edit the sample and run the NexPro program in your browser.

## Run

From the repository root, pass the sample JSON on standard input.

```sh
printf '%s\n' '{"items":[{"name":"Design","hours":2.5,"rate_cents":4000},{"name":"Testing","hours":1,"rate_cents":2500}],"discount_percent":10}' | nexpro run projects/freelance-quote/main.pa
```

To run in the [NexPro Playground](https://nexpro-playground.vercel.app/), copy
`main.pa` into the editor and paste the sample JSON into **Program input**.

## Sample input

```json
{"items":[{"name":"Design","hours":2.5,"rate_cents":4000},{"name":"Testing","hours":1,"rate_cents":2500}],"discount_percent":10}
```

## Expected output

```json
{
  "items": [
    {
      "name": "Design",
      "cost_cents": 10000
    },
    {
      "name": "Testing",
      "cost_cents": 2500
    }
  ],
  "subtotal_cents": 12500,
  "discount_cents": 1250,
  "total_cents": 11250
}
```

Hourly rates are integer cents and hours can be fractional. Each line and the final discount use `std/math.round()` to the nearest cent. The discount defaults to 0%.
