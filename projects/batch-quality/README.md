# Production Batch Quality Review

Classifies CSV production batches against a maximum rejection rate. [Read the NexPro code](main.pa)

[Open the live form](https://nexpro-playground.vercel.app/projects/batch-quality/) to edit the sample and run the program in your browser.

**NexPro features.** Required CSV headers, typed batches, record rules, and separate file and row errors.

## Run

Use NexPro 4.9 or later. From the repository root, run the following command.

```sh
printf '%s\n' '{"max_percent":5,"csv":"id,sampled,rejected\nB-01,100,2\nB-02,20,3\nB-03,10,11"}' | nexpro run projects/batch-quality/main.pa
```

You can also select **Production Batch Quality Review** under **Examples → NexPro projects** in the
[Playground](https://nexpro-playground.vercel.app/).

## Sample input

```json
{
  "max_percent": 5,
  "csv": "id,sampled,rejected\nB-01,100,2\nB-02,20,3\nB-03,10,11"
}
```

## Expected output

```json
{
  "released": [
    {
      "id": "B-01",
      "rejection_percent": 2
    }
  ],
  "held": [
    {
      "id": "B-02",
      "rejection_percent": 15
    }
  ],
  "row_issues": [
    {
      "row": 4,
      "code": "record_rule"
    }
  ],
  "file_error": null
}
```

The threshold is inclusive. Try removing the rejected header to see the file-level error.
