# Critical Path Scheduler

Calculates earliest task starts, total duration, and a critical path from task dependencies. [Read the NexPro code](main.pa)

[Open the live form](https://nexpro-playground.vercel.app/projects/critical-path/) to edit the sample and run the NexPro program in your browser.

## Run

Use NexPro 4.9 or later. Save the sample below as `input.json` and run from the repository root.

```sh
nexpro run projects/critical-path/main.pa < input.json
```

## Sample input

```json
[
  {
    "id": "Launch",
    "duration": 1,
    "after": [
      "Build",
      "Review"
    ]
  },
  {
    "id": "Design",
    "duration": 2,
    "after": []
  },
  {
    "id": "Review",
    "duration": 2,
    "after": [
      "Design"
    ]
  },
  {
    "id": "Build",
    "duration": 5,
    "after": [
      "Design"
    ]
  }
]
```

## Expected output

```json
{
  "schedule": [
    {
      "id": "Design",
      "start": 0,
      "finish": 2
    },
    {
      "id": "Review",
      "start": 2,
      "finish": 4
    },
    {
      "id": "Build",
      "start": 2,
      "finish": 7
    },
    {
      "id": "Launch",
      "start": 7,
      "finish": 8
    }
  ],
  "duration": 8,
  "critical_path": [
    "Design",
    "Build",
    "Launch"
  ]
}
```

Tasks can appear in any order. Independent tasks may run at the same time. Durations are nonnegative whole units. Missing dependencies, repeated IDs, and cycles produce structured errors. Equal-length paths are resolved using the given dependency and task order.
