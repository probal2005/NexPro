import subprocess

tests = [
    "tests/test_lexer.py",
    "tests/test_parser.py",
    "tests/test_interpreter.py",
    "tests/test_examples.py",
]

for test in tests:

    print("=" * 60)
    print(test)
    print("=" * 60)

    subprocess.run(["python", test])

print("\nAll Tests Completed ✅")