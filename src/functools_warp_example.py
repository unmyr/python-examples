#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""nop example."""
import functools


def my_decorator(f):
    """My decorator."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        print("BEGIN")
        ret = f(*args, **kwargs)
        print("END")
        return ret

    return wrapper


@my_decorator
def hello():
    """Run main."""
    print("Hello world")


if __name__ == '__main__':
    hello()

# EOF
