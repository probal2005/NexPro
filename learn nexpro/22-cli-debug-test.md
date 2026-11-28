# 22. CLI, tests, and debugging

[← Previous lesson](21-sharing.md) · [Course index](README.md) · [Next lesson →](23-capstone.md)

The interpreter runs .pa source. The compiler converts that source into standalone Python.

## Types and syntax

| Type | Syntax | Definition |
|---|---|---|
| Installation | Wheel file and Python 3.11 or newer | Sets up the NexPro CLI. |
| Run and check | `nexpro run main.pa`, `nexpro check main.pa` | Runs a program or checks syntax and imports. |
| Compile | `nexpro compile main.pa -o main.py` | Generates a Python script. |
| Project commands | `nexpro init`, `nexpro test` | Scaffolds a project and runs project tests. |
| Debugging | Playground Trace execution or VS Code debugging | Shows execution steps or lets you set breakpoints and inspect variables. |

## When and why to use it

Run the example as main.pa. Then run it with Trace execution in the Playground to see the order of statements.

**Advantages.** You can check the same program in the CLI, the Playground, and generated Python.

**Limitations and common mistakes.** Syntax checks cannot verify a business rule. Test that rule with different inputs and expected outputs.

## Try it

Paste this code into the [Playground](https://nexpro-playground.vercel.app/) and select **Run code**. [Download the example .pa file](examples/22-cli-debug-test.pa)

[CLI installation guide](../docs/HELP.md) · [VS Code debugging](../editors/vscode/README.md)

```text
function subtotal(price, quantity)
    return price * quantity
end
assert subtotal(50, 3) == 150
say subtotal(50, 3)
```

**Expected result**

```text
150
```

## Exercise

Change the expected value in the assertion from 150 to 140.

<details>
<summary>Show the answer</summary>

The assertion fails. The error reports the .pa source location.

</details>

[← Previous lesson](21-sharing.md) · [Course index](README.md) · [Next lesson →](23-capstone.md)
