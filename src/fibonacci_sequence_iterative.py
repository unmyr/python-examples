# -*- coding: utf-8 -*-
"""Calculate the fibonacci sequence."""
from sys import argv
import cProfile
import pstats
import typing


def fib(number: int) -> typing.Optional[int]:
    """Calculate the fibonacci sequence."""
    if number < 0:
        return None

    a_n1 = 0
    a_n2 = 1
    for _ in range(1, number + 1):
        a_n1, a_n2 = a_n2, a_n1 + a_n2
    return a_n1


def main(num: int) -> typing.Optional[int]:
    """Run main."""
    pr: cProfile.Profile
    pr = cProfile.Profile()

    pr.enable()
    ret_val = fib(num)
    pr.disable()
    print(ret_val)

    stats: pstats.Stats = pstats.Stats(pr)
    stats.sort_stats("tottime")
    stats.print_stats(100)

    return ret_val


if __name__ == "__main__":
    main(int(argv[1]))

# EOF
