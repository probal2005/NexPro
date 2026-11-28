# Quiz & Score Tracker

Scores answers and reports mistakes and unanswered questions. [Read the NexPro code](main.pa)

[Open the live form](https://nexpro-playground.vercel.app/projects/quiz-score/) to edit the sample and run the NexPro program in your browser.

## Run

From the repository root, pass the sample JSON on standard input.

```sh
printf '%s\n' '{"questions":[{"question":"Capital of France?","answer":"Paris"},{"question":"2 + 2?","answer":"4"},{"question":"Red Planet?","answer":"Mars"}],"answers":[" paris ","5"]}' | nexpro run projects/quiz-score/main.pa
```

To run in the [NexPro Playground](https://nexpro-playground.vercel.app/), copy
`main.pa` into the editor and paste the sample JSON into **Program input**.

## Sample input

```json
{"questions":[{"question":"Capital of France?","answer":"Paris"},{"question":"2 + 2?","answer":"4"},{"question":"Red Planet?","answer":"Mars"}],"answers":[" paris ","5"]}
```

## Expected output

```json
{
  "correct": 1,
  "total": 3,
  "mistakes": [
    {
      "question": "2 + 2?",
      "submitted": "5",
      "correct": "4"
    },
    {
      "question": "Red Planet?",
      "submitted": "",
      "correct": "Mars"
    }
  ]
}
```

Answers match questions by position. Text comparisons ignore outer whitespace and letter case. An omitted trailing answer counts as unanswered.
