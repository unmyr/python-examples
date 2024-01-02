# -*- coding: utf-8 -*-
"""Calculate the fibonacci sequence."""
from sys import argv
import cProfile
import pstats


def fib(number: int) -> int:
    """Calculate fibonacci sequence."""
    if number == 0:
        return 0
    if number == 1:
        return 1
    return fib(number - 2) + fib(number - 1)


def main(num: int) -> int:
    """Run main."""
    pr: cProfile.Profile
    pr = cProfile.Profile()

    pr.enable()
    ret_val = fib(num)
    pr.disable()
    print(ret_val)

    stats: pstats.Stats = pstats.Stats(pr)
    stats.sort_stats("cumtime")
    stats.print_stats(100)

    return ret_val


if __name__ == "__main__":
    main(int(argv[1]))

# EOF
