#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Example of math."""
import math

if __name__ == "__main__":
    VMIN = -5.1
    VMAX = 10.1
    print("VMIN: %f, VMAX: %f" % (VMIN, VMAX))

    exponent, remainder = divmod(math.log10(VMAX - VMIN), 1)
    print("exponent %f, remainder: %f" % (exponent, remainder))
    if remainder < 0.5:
        exponent -= 1
    print("exponent %f, remainder: %f" % (exponent, remainder))

    scale = 10 ** (-exponent)
    print("exponent %f, remainder: %f, scale: %f" % (
      exponent, remainder, scale))

    VMIN = math.floor(scale * VMIN) / scale
    VMAX = math.ceil(scale * VMAX) / scale

    print("VMIN: %f, VMAX: %f" % (VMIN, VMAX))
