# NexPro grammar

```text
program        -> (import | function | statement)* EOF
import         -> "import" STRING
function       -> "function" IDENTIFIER "(" parameters? ")" function_body "end"
parameters     -> IDENTIFIER ("," IDENTIFIER)*
function_body  -> statement*
block          -> statement*
statement      -> IDENTIFIER "=" expression
                | "say" expression
                | "if" expression block ("else" block)? "end"
                | "while" expression block "end"
                | "for" IDENTIFIER "in" expression block "end"
                | "break" | "continue"
                | "return" expression
                | call
expression     -> logical_and ("or" logical_and)*
logical_and    -> logical_not ("and" logical_not)*
logical_not    -> "not" logical_not | comparison
comparison     -> addition (comparison_op addition)?
comparison_op  -> "==" | "!=" | "<" | "<=" | ">" | ">="
addition       -> multiplication (("+" | "-") multiplication)*
multiplication -> unary (("*" | "/") unary)*
unary          -> ("+" | "-") unary | postfix
postfix        -> primary ("[" expression "]")*
list           -> "[" arguments? "]"
primary        -> NUMBER | STRING | "true" | "false"
                | list | call | IDENTIFIER | "(" expression ")"
call           -> IDENTIFIER "(" arguments? ")"
arguments      -> expression ("," expression)*
```

A `return` statement is valid only inside a function, including a nested
`if` or `while` block within that function.

`break` and `continue` are valid only inside a loop.
