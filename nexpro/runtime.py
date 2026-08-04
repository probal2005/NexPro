"""
NexPro Programming Language
Runtime Environment
Version 0.4.0
Author: Probal Dhali
"""

from nexpro.errors import NexProRuntimeError


class Runtime:
    """
    Runtime Environment

    Stores all variables during execution.
    """

    def __init__(self):

        self.variables = {}

    # ------------------------------------------

    def exists(self, name):

        return name in self.variables

    # ------------------------------------------

    def set(self, name, value):

        self.variables[name] = value

    # ------------------------------------------

    def get(self, name):

        if name not in self.variables:

            raise NexProRuntimeError(
                f"Undefined variable '{name}'"
            )

        return self.variables[name]

    # ------------------------------------------

    def remove(self, name):

        if name in self.variables:

            del self.variables[name]

    # ------------------------------------------

    def clear(self):

        self.variables.clear()

    # ------------------------------------------

    def dump(self):

        return dict(self.variables)

    # ------------------------------------------

    def __repr__(self):

        return f"Runtime({self.variables})"