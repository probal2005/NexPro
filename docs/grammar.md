expression
    -> addition

------------------------------------

addition
    -> multiplication
       ( (PLUS | MINUS)
         multiplication )*

------------------------------------

multiplication
    -> primary
       ( (STAR | SLASH)
         primary )*

------------------------------------

primary
    -> NUMBER

    | STRING

    | IDENTIFIER

    | "(" expression ")"