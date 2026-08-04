from nexpro.runtime import Runtime

runtime = Runtime()

runtime.set("name", "Probal")

runtime.set("age", 20)

print(runtime.get("name"))

print(runtime.get("age"))

print(runtime.dump())