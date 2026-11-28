# 27. Queues, linked lists, and statistics

[← Previous lesson](26-error-recovery.md) · [Course index](README.md) · [Next lesson →](28-structured-errors.md)

Introduced in NexPro 4.0.

A queue processes the oldest item first. A singly linked list connects items in order. Statistics summarize numeric lists or groups of records.

## Syntax and behavior

- `std/queue` provides `new`, `enqueue`, `dequeue`, `peek`, and `to_list`.
- `std/linked_list` provides `new`, `append`, `insert`, `remove`, and `to_list`.
- `std/stats` provides `mean`, `median`, and `count_by`.

## When to use it

Process dispatch orders in arrival order and report item counts by team.

Queue removal takes the front item, and linked-list insertion can update a chain in place. Reading or removing from an empty queue raises an error. Mean and median require non-empty finite numeric input.

## Try it

Paste the code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**, or run the [.pa example](../examples/dispatch_summary.pa) with `nexpro run`.

```text
import "std/queue" as queue
import "std/linked_list" as linked
import "std/stats" as stats

pending = queue.new([
    {"team": "North", "items": 4},
    {"team": "South", "items": 8},
    {"team": "North", "items": 6}
])
history = linked.new()
quantities = []
while len(pending) > 0
    order = queue.dequeue(pending)
    linked.append(history, order)
    append(quantities, order["items"])
end
say stats.count_by(linked.to_list(history), "team")
say stats.mean(quantities)
say stats.median(quantities)
```

**Expected output**

```text
{'North': 2, 'South': 1}
6
6
```

## Exercise

Change the third order to the South team.

<details>
<summary>Show the answer</summary>

South has two orders. Mean and median remain 6 because the quantities stayed the same.

</details>

[← Previous lesson](26-error-recovery.md) · [Course index](README.md) · [Next lesson →](28-structured-errors.md)
