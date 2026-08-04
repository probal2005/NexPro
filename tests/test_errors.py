from nexpro.errors import NexProSyntaxError

try:
    raise NexProSyntaxError(
        "Demo Error",
        line=5,
        column=12,
        filename="demo.pa",
    )

except Exception as e:
    print(e)