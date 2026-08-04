"""
NexPro Interpreter
"""


def execute(ast):

    for node in ast:

        if node[0] == "SAY":

            print(node[1])
