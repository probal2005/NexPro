# 21. Playground actions and sharing

[← Previous lesson](20-csv-tools.md) · [Course index](README.md) · [Next lesson →](22-cli-debug-test.md)

The Playground can share source code or a form generated from that source.

## Types and syntax

| Type | Syntax | Definition |
|---|---|---|
| Check syntax | More menu | Checks parsing and imports. |
| Compile to Python | More menu | Generates standalone Python source. |
| Share code | More menu | Opens the source and modules in the recipient's editor. |
| Share tool | More menu | Creates a link to a standalone tool page. |
| View source | Tool page action | Displays the source and offers a link back to the Playground. |

## When and why to use it

Paste the example into the Playground and select **More → Share tool**. Open the link in a new tab and choose Start tool.

**Advantages.** The recipient can use the form without working in an editor and inspect the source when needed.

**Limitations and common mistakes.** The link carries source, attached modules, and defaults written into the source. Form input and uploaded CSV data stay out of the link. The JSON payload limit is 12,000 bytes.

## Try it

Paste this code into the [Playground](https://nexpro-playground.vercel.app/) and select **Preview tool**. [Download the example .pa file](examples/21-sharing.pa)

```text
amount = number_field("Amount", 20, 0)
result("Double", amount * 2)
```

**Expected result**

```text
Double: 40
```

## Exercise

Set Amount to 30, then reopen the original share link.

<details>
<summary>Show the answer</summary>

The original link still uses the default of `20`.

</details>

[← Previous lesson](20-csv-tools.md) · [Course index](README.md) · [Next lesson →](22-cli-debug-test.md)
