"""
NexPro Runtime
Version 0.3.0
"""


class Runtime:

    def __init__(self):

        self.variables = {}

    # --------------------------

    def set(self, name, value):

        self.variables[name] = value

    # --------------------------

    def get(self, name):

        if name not in self.variables:

            raise NameError(
                f"Variable '{name}' is not defined."
            )

        return self.variables[name]