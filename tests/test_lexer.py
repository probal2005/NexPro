"""
NexPro Programming Language
Universal Lexer Test
Version 0.4.0+
Author: Probal Dhali
"""

import sys
from pathlib import Path

# -------------------------------------------------------
# Add project root to Python path
# -------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))

# -------------------------------------------------------

from nexpro.lexer import Lexer

# -------------------------------------------------------


def print_header(title):

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# -------------------------------------------------------

def test_lexer(filename):

    print_header(f"Testing : {filename}")

    try:

        with open(filename, "r", encoding="utf-8") as file:
            source = file.read()

    except FileNotFoundError:

        print(f"File not found : {filename}")
        return

    print("\nSource Code\n")
    print(source)

    lexer = Lexer(source)

    print_header("Tokens")

    try:

        tokens = lexer.tokenize()

        for index, token in enumerate(tokens, start=1):

            print(f"{index:03d}  {token}")

        print_header("Result")

        print("✓ Lexer Test Passed")

    except Exception as error:

        print_header("Lexer Error")

        print(error)


# -------------------------------------------------------

def main():

    if len(sys.argv) == 1:

        print(
            """
Usage

python tests/test_lexer.py <source.pa>

Examples

python tests/test_lexer.py examples/variables.pa

python tests/test_lexer.py examples/numbers.pa

python tests/test_lexer.py examples/string.pa

python tests/test_lexer.py examples/operators.pa

python tests/test_lexer.py examples/if.pa

python tests/test_lexer.py examples/while.pa
"""
        )

        return

    filename = sys.argv[1]

    test_lexer(filename)


# -------------------------------------------------------

if __name__ == "__main__":

    main()