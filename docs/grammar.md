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
                | "break"
                | "return" expression
                | call
expression     -> addition (comparison addition)?
comparison     -> "==" | "!=" | "<" | "<=" | ">" | ">="
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

A `break` statement is valid only inside a loop.
