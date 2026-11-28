# Warranty Claim Triage

Processes warranty claims in arrival order and separates covered, expired, and invalid requests. [Read the NexPro code](main.pa)

[Open the live form](https://nexpro-playground.vercel.app/projects/warranty-triage/) to edit the sample and run the program in your browser.

**NexPro features.** FIFO queues, typed claims, and per-claim error recovery.

## Run

Use NexPro 4.9 or later. From the repository root, run the following command.

```sh
printf '%s\n' '{"coverage_days":365,"claims":[{"id":"W-01","age_days":365},{"id":"W-02","age_days":366},{"id":"W-03","age_days":-1}]}' | nexpro run projects/warranty-triage/main.pa
```

You can also select **Warranty Claim Triage** under **Examples → NexPro projects** in the
[Playground](https://nexpro-playground.vercel.app/).

## Sample input

```json
{
  "coverage_days": 365,
  "claims": [
    {
      "id": "W-01",
      "age_days": 365
    },
    {
      "id": "W-02",
      "age_days": 366
    },
    {
      "id": "W-03",
      "age_days": -1
    }
  ]
}
```

## Expected output

```json
{
  "covered": [
    "W-01"
  ],
  "expired": [
    "W-02"
  ],
  "invalid": [
    {
      "id": "W-03",
      "message": "Claim age cannot be negative"
    }
  ]
}
```

The coverage limit is inclusive. Negative ages are reported separately.
