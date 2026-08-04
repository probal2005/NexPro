"""
NexPro Parser
v0.2.0
"""


def parse(tokens):

    ast = []

    for token in tokens:

        if token["type"] == "ASSIGN":

            ast.append({

                "node": "ASSIGN",

                "name": token["name"],

                "value": token["value"]

            })

        elif token["type"] == "SAY_STRING":

            ast.append({

                "node": "SAY_STRING",

                "value": token["value"]

            })

        elif token["type"] == "SAY_VARIABLE":

            ast.append({

                "node": "SAY_VARIABLE",

                "value": token["value"]

            })

    return ast