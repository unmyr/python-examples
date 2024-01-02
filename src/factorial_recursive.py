# -*- coding: utf-8 -*-
"""Calculate the factorial of a number."""
from sys import argv


def factorial(number: int) -> int:
    """Calculate factorial."""
    if number == 0:
        return 1
    return number * factorial(number - 1)


if __name__ == "__main__":
    print(factorial(int(argv[1])))

# EOF
