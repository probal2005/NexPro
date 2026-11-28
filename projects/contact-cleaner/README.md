# Contact List Cleaner

Trims contact fields and identifies duplicate or incomplete rows. [Read the NexPro code](main.pa)

## Run

From the repository root, pass the sample JSON on standard input.

```sh
printf '%s\n' '[{"name":" Ada ","email":" ADA@example.com ","phone":" 1234 "},{"name":"Ada again","email":"ada@example.com","phone":"4567"},{"name":"Ben","phone":"2222"}]' | nexpro run projects/contact-cleaner/main.pa
```

To run in the [NexPro Playground](https://nexpro-playground.vercel.app/), copy
`main.pa` into the editor and paste the sample JSON into **Program input**.

## Sample input

```json
[{"name":" Ada ","email":" ADA@example.com ","phone":" 1234 "},{"name":"Ada again","email":"ada@example.com","phone":"4567"},{"name":"Ben","phone":"2222"}]
```

## Expected output

```json
{
  "contacts": [
    {
      "name": "Ada",
      "email": "ada@example.com",
      "phone": "1234"
    }
  ],
  "duplicates": [
    {
      "row": 2,
      "first_row": 1
    }
  ],
  "incomplete": [
    3
  ]
}
```

Email deduplication is case-insensitive and retains the first complete row. Row numbers start at 1.
