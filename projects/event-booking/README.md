# Event Seat Booking

Accepts seat requests in order while enforcing the event capacity. [Read the NexPro code](main.pa)

[Open the live form](https://nexpro-playground.vercel.app/projects/event-booking/) to edit the sample and run the program in your browser.

**NexPro features.** Typed booking requests, record rules, and validated dot assignment.

## Run

Use NexPro 4.9 or later. From the repository root, run the following command.

```sh
printf '%s\n' '{"capacity":5,"requests":[{"name":"Ada","seats":3},{"name":"Grace","seats":3},{"name":"Linus","seats":2}]}' | nexpro run projects/event-booking/main.pa
```

You can also select **Event Seat Booking** under **Examples → NexPro projects** in the
[Playground](https://nexpro-playground.vercel.app/).

## Sample input

```json
{
  "capacity": 5,
  "requests": [
    {
      "name": "Ada",
      "seats": 3
    },
    {
      "name": "Grace",
      "seats": 3
    },
    {
      "name": "Linus",
      "seats": 2
    }
  ]
}
```

## Expected output

```json
{
  "reserved": 5,
  "remaining": 0,
  "accepted": [
    "Ada",
    "Linus"
  ],
  "rejected": [
    {
      "name": "Grace",
      "message": "Booking exceeds capacity"
    }
  ]
}
```

A rejected reservation leaves the available seats unchanged, so the next request can still use them.
