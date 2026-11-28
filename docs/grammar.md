# NexPro grammar

```text
program        -> (import | function | record | statement)* EOF
import         -> "import" STRING ("as" IDENTIFIER)?
function       -> "function" IDENTIFIER "(" parameters? ")" function_body "end"
record         -> "record" IDENTIFIER "(" fields? ")" rule*
rule           -> "where" STRING "," expression "," STRING
fields         -> field ("," field)*
field          -> IDENTIFIER (":" (IDENTIFIER | "null"))? ("=" expression)?
parameters     -> parameter ("," parameter)*
parameter      -> IDENTIFIER ("=" expression)?
function_body  -> statement*
block          -> statement*
statement      -> assignment
                | "say" expression
                | "if" expression block ("elif" expression block)* ("else" block)? "end"
                | "while" expression block "end"
                | "for" IDENTIFIER "in" expression block "end"
                | "break" | "continue"
                | "assert" expression
                | "try" block "catch" (IDENTIFIER | "(" IDENTIFIER ")") block "end"
                | "throw" expression ("," expression)?
                | "return" expression
                | call
assignment     -> IDENTIFIER ("[" expression "]" | "." IDENTIFIER)* "=" expression
expression     -> logical_and ("or" logical_and)*
logical_and    -> logical_not ("and" logical_not)*
logical_not    -> "not" logical_not | comparison
comparison     -> addition (comparison_op addition)?
comparison_op  -> "==" | "!=" | "<" | "<=" | ">" | ">="
addition       -> multiplication (("+" | "-") multiplication)*
multiplication -> unary (("*" | "/" | "//" | "%") unary)*
unary          -> ("+" | "-") unary | power
power          -> postfix ("**" unary)?
postfix        -> primary ("[" subscript "]" | "." IDENTIFIER)*
subscript      -> expression | expression? ":" expression? (":" expression?)?
list           -> "[" arguments? "]"
dictionary     -> "{" (entry ("," entry)*)? "}"
entry          -> expression ":" expression
primary        -> NUMBER | STRING | "true" | "false" | "null"
                | dictionary | list | call | member | IDENTIFIER | "(" expression ")"
member         -> IDENTIFIER "." IDENTIFIER
call           -> (IDENTIFIER | member) "(" call_arguments? ")"
call_arguments -> call_argument ("," call_argument)*
call_argument  -> (IDENTIFIER "=")? expression
arguments      -> expression ("," expression)*
```

A `return` statement is valid only inside a function, including a nested
`if` or `while` block within that function.

`break` and `continue` are valid only inside a loop.
