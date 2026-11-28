# 08. Conditionals with if, else, and end

[← Previous lesson](07-logic.md) · [Course index](README.md) · [Next lesson →](09-loops.md)

An if block runs when its condition is true. An optional else block handles the other case.

## Types and syntax

| Type | Syntax | Definition |
|---|---|---|
| If | `if condition … end` | Runs a block conditionally. |
| If and else | `if condition … else … end` | Chooses one of two blocks. |
| Nested if | An if inside a block | Adds another decision within a branch. |

## When and why to use it

Choose a result such as Pass, Distinction, or Retry from a numeric score.

**Advantages.** Each branch can express a business rule directly.

**Limitations and common mistakes.** Every if needs an end. Use `elif condition` to test additional branches before `else`.

## Try it

Paste this code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**. [Download the example .pa file](examples/08-conditionals.pa)

```text
score = 78
if score >= 80
    say "Distinction"
else
    if score >= 50
        say "Pass"
    else
        say "Retry"
    end
end
```

**Expected result**

```text
Pass
```

## Exercise

Try scores of 50, 80, and 49.

<details>
<summary>Show the answer</summary>

The results are `Pass`, `Distinction`, and `Retry`, respectively.

</details>

[← Previous lesson](07-logic.md) · [Course index](README.md) · [Next lesson →](09-loops.md)
