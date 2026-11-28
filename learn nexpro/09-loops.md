# 09. Loops, break, and continue

[← Previous lesson](08-conditionals.md) · [Course index](README.md) · [Next lesson →](10-strings.md)

A for loop visits items in order. A while loop repeats while a condition holds.

## Types and syntax

| Type | Syntax | Definition |
|---|---|---|
| For | `for item in items … end` | Visits list items, string characters, or dictionary keys. |
| While | `while condition … end` | Rechecks the condition before each iteration. |
| Break | `break` | Exits the nearest loop. |
| Continue | `continue` | Skips the rest of the current iteration. |

## When and why to use it

Process many records with one rule, such as skipping invalid entries before totaling the rest.

**Advantages.** One loop can handle a collection of any length.

**Limitations and common mistakes.** A while loop can run indefinitely if its condition never becomes false. A for loop may see items added to the list it is visiting.

## Try it

Paste this code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**. [Download the example .pa file](examples/09-loops.pa)

```text
total = 0
for score in [4, -1, 6, 0, 9]
    if score < 0
        continue
    end
    if score == 0
        break
    end
    total = total + score
end
say total
count = 2
while count > 0
    say count
    count = count - 1
end
```

**Expected result**

```text
10
2
1
```

## Exercise

Does the loop add the 9 that follows the 0?

<details>
<summary>Show the answer</summary>

No. The break exits the loop when it reaches 0.

</details>

[← Previous lesson](08-conditionals.md) · [Course index](README.md) · [Next lesson →](10-strings.md)
