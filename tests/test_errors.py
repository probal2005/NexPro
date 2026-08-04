from nexpro.errors import LexerError

try:

    raise LexerError(

        "Unknown character '$'",

        line=4,

        column=10,

        filename="demo.pa",

    )

except Exception as error:

    print(error)