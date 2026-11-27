# Your first NexPro program

Install NexPro with the [installation guide](HELP.md), or use the
[online playground](https://nexpro-playground.vercel.app/).

## Print a message

Create `hello.pa` and save it as UTF-8 text.

```text
say "Hello NexPro!"
```

Run `nexpro check hello.pa` to check syntax and `nexpro run hello.pa` to print
the message. In the playground, paste the code and select **Run code**.

## Calculate an average

Create `average.pa`. Each call to `input()` reads one line as text. The
`float()` calls convert that text before the values are added.

```text
function average(scores)
    total = 0
    position = 0
    while position < len(scores)
        total = total + scores[position]
        position = position + 1
    end
    return total / len(scores)
end

scores = [float(input()), float(input()), float(input())]
say average(scores)
```

Run `nexpro run average.pa` and enter `70`, `85`, and `100` on separate lines.
In the playground, put those three lines in **Program input** before running.
The program prints `85.0`.

## Compile it to Python

```sh
nexpro compile average.pa -o average.py
python average.py
```

Enter the same three values when running the compiled script. The playground's
**Compile to Python** and **Download .py** buttons produce the same kind of file.

To see how programs reuse code across files, try the playground example
**Import math functions** or run the repository's [import example](../examples/imports.pa).
