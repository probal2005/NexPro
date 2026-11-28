# Tournament Standings

Builds a league table from teams and recorded scores. [Read the NexPro code](main.pa)

[Open the live form](https://nexpro-playground.vercel.app/projects/tournament-standings/) to edit the sample and run the NexPro program in your browser.

## Run

From the repository root, pass the sample JSON on standard input.

```sh
printf '%s\n' '{"teams":["Lions","Owls","Foxes"],"matches":[{"home":"Lions","away":"Owls","home_goals":2,"away_goals":1},{"home":"Owls","away":"Foxes","home_goals":0,"away_goals":0},{"home":"Foxes","away":"Lions","home_goals":1,"away_goals":1}]}' | nexpro run projects/tournament-standings/main.pa
```

To run in the [NexPro Playground](https://nexpro-playground.vercel.app/), copy
`main.pa` into the editor and paste the sample JSON into **Program input**.

## Sample input

```json
{"teams":["Lions","Owls","Foxes"],"matches":[{"home":"Lions","away":"Owls","home_goals":2,"away_goals":1},{"home":"Owls","away":"Foxes","home_goals":0,"away_goals":0},{"home":"Foxes","away":"Lions","home_goals":1,"away_goals":1}]}
```

## Expected output

```json
{
  "standings": [
    {
      "team": "Lions",
      "played": 2,
      "points": 4,
      "goal_difference": 1,
      "goals_for": 3
    },
    {
      "team": "Foxes",
      "played": 2,
      "points": 2,
      "goal_difference": 0,
      "goals_for": 1
    },
    {
      "team": "Owls",
      "played": 2,
      "points": 1,
      "goal_difference": -1,
      "goals_for": 1
    }
  ]
}
```

A win earns three points and a draw earns one. Ties are ordered by goal difference, goals scored, then team name. Attach [standings.pa](standings.pa) in the Playground, or run `nexpro run projects/tournament-standings/test_standings.pa` to try the native tests.
