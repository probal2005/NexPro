# NexPro grammar

```text
program        -> (import | function | statement)* EOF
import         -> "import" STRING ("as" IDENTIFIER)?
function       -> "function" IDENTIFIER "(" parameters? ")" function_body "end"
parameters     -> IDENTIFIER ("," IDENTIFIER)*
function_body  -> statement*
block          -> statement*
statement      -> assignment
                | "say" expression
                | "if" expression block ("else" block)? "end"
                | "while" expression block "end"
                | "for" IDENTIFIER "in" expression block "end"
                | "break" | "continue"
                | "assert" expression
                | "return" expression
                | call
assignment     -> IDENTIFIER ("[" expression "]")* "=" expression
expression     -> logical_and ("or" logical_and)*
logical_and    -> logical_not ("and" logical_not)*
logical_not    -> "not" logical_not | comparison
comparison     -> addition (comparison_op addition)?
comparison_op  -> "==" | "!=" | "<" | "<=" | ">" | ">="
addition       -> multiplication (("+" | "-") multiplication)*
multiplication -> unary (("*" | "/" | "//" | "%") unary)*
unary          -> ("+" | "-") unary | power
power          -> postfix ("**" unary)?
postfix        -> primary ("[" subscript "]")*
subscript      -> expression | expression? ":" expression? (":" expression?)?
list           -> "[" arguments? "]"
dictionary     -> "{" (entry ("," entry)*)? "}"
entry          -> expression ":" expression
primary        -> NUMBER | STRING | "true" | "false"
                | dictionary | list | call | member | IDENTIFIER | "(" expression ")"
member         -> IDENTIFIER "." IDENTIFIER
call           -> (IDENTIFIER | member) "(" arguments? ")"
arguments      -> expression ("," expression)*
```

A `return` statement is valid only inside a function, including a nested
`if` or `while` block within that function.

`break` and `continue` are valid only inside a loop.
