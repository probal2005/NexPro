from nexpro.ast import *

tree = Program([

    Assign(
        Variable("name"),
        String("Probal")
    ),

    Say(
        Variable("name")
    )

])

print(tree)
print(tree.statements)

print(type(tree.statements[0]).__name__)
print(type(tree.statements[1]).__name__)