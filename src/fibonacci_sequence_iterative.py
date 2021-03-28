# -*- coding: utf-8 -*-
"""Calculate the fibonacci sequence."""
from sys import argv


def fib(number: int) -> int:
    """Calculate the fibonacci sequence."""
    if number < 0:
        return None

    a_n1 = 0
    a_n2 = 1
    for _ in range(1, number + 1):
        a_n1, a_n2 = a_n2, a_n1 + a_n2
    return a_n1


if __name__ == '__main__':
    print(fib(int(argv[1])))

# EOF
