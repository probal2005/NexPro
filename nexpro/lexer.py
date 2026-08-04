"""
NexPro Lexer
v0.2.0
"""


def tokenize(code: str):
    tokens = []

    for line_number, line in enumerate(code.splitlines(), start=1):

        line = line.strip()

        if not line:
            continue

        # -------------------------
        # SAY
        # -------------------------

        if line.startswith("say "):

            value = line[4:].strip()

            if value.startswith('"') and value.endswith('"'):

                tokens.append({
                    "type": "SAY_STRING",
                    "value": value[1:-1]
                })

            else:

                tokens.append({
                    "type": "SAY_VARIABLE",
                    "value": value
                })

            continue

        # -------------------------
        # Assignment
        # -------------------------

        if "=" in line:

            name, value = line.split("=", 1)

            name = name.strip()

            value = value.strip()

            if value.startswith('"') and value.endswith('"'):

                value = value[1:-1]

            tokens.append({

                "type": "ASSIGN",

                "name": name,

                "value": value

            })

            continue

        raise SyntaxError(
            f"Line {line_number}: Unknown statement."
        )

    return tokens