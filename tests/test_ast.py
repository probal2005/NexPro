from nexpro.ast import *

tree = Program(

    [

        Assign(

            Variable("name"),

            String("Probal")

        ),

        Say(

            Variable("name")

        )

    ]

)

print(tree)