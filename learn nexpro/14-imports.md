# 14. Imports and module namespaces

[← Previous lesson](13-functions.md) · [Course index](README.md) · [Next lesson →](15-math.md)

A module is a reusable source file or a part of the standard library.

## Types and syntax

| Type | Syntax | Definition |
|---|---|---|
| Plain import | `import "rules.pa"` | Includes the module's top-level code in the same scope. |
| Aliased import | `import "rules.pa" as rules` | Gives the module its own namespace. |
| Member access | `rules.quote(50, 3)` | Calls a function or reads a top-level value through the alias. |
| Standard import | `import "std/math" as math` | Loads a module supplied by NexPro. |

## When and why to use it

Keep business rules in a separate file. Save rules.pa beside the main program locally or attach it under Module files in the Playground.

**Advantages.** Aliases help prevent naming conflicts between files.

**Limitations and common mistakes.** Paths are relative to the importing file and must stay inside the entry file's directory. Circular imports raise an error.

## Try it

Paste this code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**. [Download the example .pa file](examples/14-imports.pa)

This example also needs [rules.pa](examples/rules.pa).

```text
import "rules.pa" as rules
say rules.quote(50, 3)
say rules.currency
```

**Expected result**

```text
150
BDT
```

## Exercise

Add a service fee of 10 in rules.pa.

<details>
<summary>Show the answer</summary>

`return price * count + 10` makes the first result `160`.

</details>

[← Previous lesson](13-functions.md) · [Course index](README.md) · [Next lesson →](15-math.md)
