# Bill Splitter

Split a bill between up to 1,000 people. When the bill does not divide
evenly, some people pay one cent more so that the displayed shares add up
to the total. [Use the live calculator](https://nexpro-playground.vercel.app/projects/bill-splitter/)

- [`main.pa`](main.pa) contains the amount parsing, validation, and split.
- [`index.html`](index.html) and [`styles.css`](styles.css) define the browser form.
- [`app.js`](app.js) sends the form input to NexPro's browser worker and displays
  the returned shares.

From the repository root, run the NexPro source with the CLI.

```sh
printf '%s\n' '{"bill":"10.00","people":"3"}' | nexpro run projects/bill-splitter/main.pa
```

`bill` and `people` are strings. Use a decimal point for the bill amount, with
up to nine digits before the point and two after it. The program returns
JSON with the total and two share groups in integer cents, or an `error`
message for invalid amount or head count.

To edit and run the same source in the browser, choose **Bill Splitter** in
the [NexPro Playground](https://nexpro-playground.vercel.app/).
