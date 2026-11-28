# Student Report Card

Ranks valid students and reports empty or out-of-range score lists. [Read the NexPro code](main.pa)

## Run

From the repository root, pass the sample JSON on standard input.

```sh
printf '%s\n' '[{"name":"Ada","scores":[90,100]},{"name":"Ben","scores":[75,85]},{"name":"Chen","scores":[101]}]' | nexpro run projects/student-report-card/main.pa
```

To run in the [NexPro Playground](https://nexpro-playground.vercel.app/), copy
`main.pa` into the editor and paste the sample JSON into **Program input**.

## Sample input

```json
[{"name":"Ada","scores":[90,100]},{"name":"Ben","scores":[75,85]},{"name":"Chen","scores":[101]}]
```

## Expected output

```json
{
  "ranked": [
    {
      "name": "Ada",
      "average": 95.0,
      "grade": "A",
      "rank": 1
    },
    {
      "name": "Ben",
      "average": 80.0,
      "grade": "B",
      "rank": 2
    }
  ],
  "invalid": [
    {
      "name": "Chen",
      "reason": "Expected at least one score between 0 and 100"
    }
  ]
}
```

Scores are numeric and inclusive from 0 to 100. Grades start at 90, 80, 70, and 60 for A through D. Ranking uses the unrounded average, with input order breaking exact ties.
