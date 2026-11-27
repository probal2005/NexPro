# NexPro grammar

```text
program        -> (function | statement)* EOF
function       -> "function" IDENTIFIER "(" parameters? ")" function_body "end"
parameters     -> IDENTIFIER ("," IDENTIFIER)*
function_body  -> (statement | "return" expression)*
statement      -> IDENTIFIER "=" expression
                | "say" expression
                | call
expression     -> addition
addition       -> multiplication (("+" | "-") multiplication)*
multiplication -> unary (("*" | "/") unary)*
unary          -> ("+" | "-") unary | primary
primary        -> NUMBER | STRING | call | IDENTIFIER | "(" expression ")"
call           -> IDENTIFIER "(" arguments? ")"
arguments      -> expression ("," expression)*
```
