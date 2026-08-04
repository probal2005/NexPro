"""
NexPro Lexer
Version 0.1
"""


def tokenize(code: str):

    tokens = []

    for line in code.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith("say"):

            text = line[3:].strip()

            if text.startswith('"') and text.endswith('"'):

                text = text[1:-1]

                tokens.append(
                    ("SAY", text)
                )

            else:

                raise SyntaxError(
                    "Expected string."
                )

        else:

            raise SyntaxError(
                f"Unknown command: {line}"
            )

    return tokens
