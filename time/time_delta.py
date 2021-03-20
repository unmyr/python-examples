#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Calculate the time delta."""
import time
from datetime import datetime


def main():
    """Run main."""
    t_0 = time.time()
    time.sleep(0.8)
    t_1 = time.time()
    print(type(t_1-t_0))
    print("dt = %f" % (t_1-t_0))

    t_0 = datetime.now()
    time.sleep(0.8)
    t_1 = datetime.now()
    print(type(t_1))
    d_t = (t_0-t_1).seconds
    print("dt = %d" % d_t)


if __name__ == "__main__":
    main()
