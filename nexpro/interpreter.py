"""
NexPro Interpreter
v0.2.0
"""


memory = {}


def execute(ast):

    for node in ast:

        if node["node"] == "ASSIGN":

            memory[node["name"]] = node["value"]

        elif node["node"] == "SAY_STRING":

            print(node["value"])

        elif node["node"] == "SAY_VARIABLE":

            variable = node["value"]

            if variable not in memory:

                raise NameError(

                    f"Variable '{variable}' not defined."

                )

            print(

                memory[variable]

            )