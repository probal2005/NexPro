# Service Ticket Timeline

Applies insert and remove operations to a service ticket's note history. [Read the NexPro code](main.pa)

[Open the live form](https://nexpro-playground.vercel.app/projects/service-timeline/) to edit the sample and run the program in your browser.

**NexPro features.** Linked lists, typed edit records, and structured error codes.

## Run

Use NexPro 4.9 or later. From the repository root, run the following command.

```sh
printf '%s\n' '{"notes":["Opened","Resolved"],"edits":[{"action":"insert","position":1,"note":"Investigated"},{"action":"remove","position":0,"note":""},{"action":"remove","position":7,"note":""}]}' | nexpro run projects/service-timeline/main.pa
```

You can also select **Service Ticket Timeline** under **Examples → NexPro projects** in the
[Playground](https://nexpro-playground.vercel.app/).

## Sample input

```json
{
  "notes": [
    "Opened",
    "Resolved"
  ],
  "edits": [
    {
      "action": "insert",
      "position": 1,
      "note": "Investigated"
    },
    {
      "action": "remove",
      "position": 0,
      "note": ""
    },
    {
      "action": "remove",
      "position": 7,
      "note": ""
    }
  ]
}
```

## Expected output

```json
{
  "notes": [
    "Investigated",
    "Resolved"
  ],
  "removed": [
    "Opened"
  ],
  "issues": [
    {
      "action": "remove",
      "code": "invalid_index"
    }
  ]
}
```

Positions start at zero. A delete does not need a note.
