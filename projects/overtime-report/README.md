# Work Hours & Overtime Report

Totals weekly hours and estimates base and overtime pay. [Read the NexPro code](main.pa)

## Run

From the repository root, pass the sample JSON on standard input.

```sh
printf '%s\n' '{"employees":[{"name":"Ada","rate_cents":2000,"hours":[9,9,9,9,9]}]}' | nexpro run projects/overtime-report/main.pa
```

To run in the [NexPro Playground](https://nexpro-playground.vercel.app/), copy
`main.pa` into the editor and paste the sample JSON into **Program input**.

## Sample input

```json
{"employees":[{"name":"Ada","rate_cents":2000,"hours":[9,9,9,9,9]}]}
```

## Expected output

```json
{
  "employees": [
    {
      "name": "Ada",
      "hours": 45,
      "overtime_hours": 5,
      "pay_cents": 95000
    }
  ]
}
```

The defaults are a 40-hour threshold and a 1.5 overtime multiplier. Override them with `weekly_threshold` and `overtime_multiplier`. Rates are cents per hour. This example uses the configured rules for its calculations.
