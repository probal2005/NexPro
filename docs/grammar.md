# NexPro Grammar
Version 0.5.0

## Program

program
    -> statement*

----------------------------------------

statement
    -> assignment
    | say_statement

----------------------------------------

assignment
    -> IDENTIFIER ASSIGN expression

----------------------------------------

say_statement
    -> SAY expression

----------------------------------------

expression
    -> term
       ( (PLUS | MINUS) term )*

----------------------------------------

term
    -> factor
       ( (STAR | SLASH) factor )*

----------------------------------------

factor
    -> NUMBER
    | STRING
    | IDENTIFIER
    | LPAREN expression RPAREN