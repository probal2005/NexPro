# 24. Text, list, and dictionary modules

[← Previous lesson](23-capstone.md) · [Course index](README.md) · [Next lesson →](25-optional-values.md)

Introduced in NexPro 3.7.

Collection helpers clean text, edit lists, and combine dictionaries.

## Syntax and behavior

- `std/text` offers `replace`, `find`, `contains`, `starts_with`, and `ends_with`.
- `std/list` offers `insert`, `pop`, and `remove` for editing, plus `unique` for a new list.
- `std/dict` offers `has` and `remove` for existing entries, plus `merge` for a new dictionary.

## When to use it

Clean imported names, deduplicate item codes, or merge options with defaults.

These helpers replace common manual loops. List edits change the original list. Dictionary merges are shallow, and right-hand values win.

## Try it

Paste the code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**, or run the [.pa example](examples/24-collection-modules.pa) with `nexpro run`.

```text
import "std/text" as text
import "std/list" as lists
import "std/dict" as records

say text.replace("Ada  Smith", "  ", " ")
say lists.unique(["A", "B", "A"])
say records.merge({"count": 0}, {"count": 2})
```

**Expected output**

```text
Ada Smith
['A', 'B']
{'count': 2}
```

## Exercise

Change the duplicate item code to C.

<details>
<summary>Show the answer</summary>

All three codes are now distinct.

</details>

[← Previous lesson](23-capstone.md) · [Course index](README.md) · [Next lesson →](25-optional-values.md)
