# -*- coding: utf-8 -*-
"""Calculate the fibonacci sequence."""
from sys import argv


def fib(number: int) -> int:
    """Calculate fibonacci sequence."""
    if number == 0:
        return 0
    if number == 1:
        return 1
    return fib(number - 2) + fib(number - 1)


if __name__ == '__main__':
    print(fib(int(argv[1])))

# EOF
