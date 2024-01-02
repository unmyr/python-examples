# -*- coding: utf-8 -*-
"""Calculate the factorial of a number."""
from sys import argv
import typing


def factorial(number: int) -> typing.Optional[int]:
    """Calculate factorial."""
    if number < 0:
        return None

    factor = 1
    for n_cur in range(1, number + 1):
        factor *= n_cur
    return factor


if __name__ == "__main__":
    print(factorial(int(argv[1])))

# EOF
