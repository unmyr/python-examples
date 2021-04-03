#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Example of math."""
import math

if __name__ == "__main__":
    V_MIN = -5.1
    V_MAX = 10.1
    print("V_MIN: %f, V_MAX: %f" % (V_MIN, V_MAX))

    exponent, remainder = divmod(math.log10(V_MAX - V_MIN), 1)
    print("exponent %f, remainder: %f" % (exponent, remainder))
    if remainder < 0.5:
        exponent -= 1
    print("exponent %f, remainder: %f" % (exponent, remainder))

    scale = 10 ** (-exponent)
    print("exponent %f, remainder: %f, scale: %f" % (
        exponent, remainder, scale))

    V_MIN = math.floor(scale * V_MIN) / scale
    V_MAX = math.ceil(scale * V_MAX) / scale

    print("V_MIN: %f, V_MAX: %f" % (V_MIN, V_MAX))
