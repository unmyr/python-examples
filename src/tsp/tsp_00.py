#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Run tsp_00."""
import math

import matplotlib.pyplot as plt
import numpy as np


def main():
    """Run main."""
    p_x = np.random.randn(30)
    p_y = np.sin(p_x) + np.random.randn(p_x.size)
    points = np.empty(p_x.size, np.int8)
    for i in range(p_x.size):
        points[i] = i

    plt.plot(p_x, p_y)  # "o"は小さい円(circle marker)
    plt.savefig("tsp_before.png")
    plt.clf()

    distance_table = np.empty((p_x.size, p_x.size), np.float32)

    print("calc distance ...")
    for i in range(p_x.size):
        for j in range(p_x.size):
            if i == j:
                distance_table[i][j] = 0
            else:
                d_x = p_x[j] - p_x[i]
                d_y = p_y[j] - p_y[i]
                distance_table[i][j] = math.sqrt(d_x * d_x + d_y * d_y)

    total_before = 0.0
    i = 0
    while i < (p_x.size - 1):
        total_before += distance_table[i][i + 1]
        i += 1

    print("opt-2 ...")
    i = 0
    while True:
        count = 0
        while i < p_x.size:
            j = i + 2
            while True:
                if p_x.size < j:
                    break
                w_1 = distance_table[i % p_x.size][(i + 1) % p_x.size]
                w_2 = distance_table[j % p_x.size][(j + 1) % p_x.size]
                w_3 = distance_table[i % p_x.size][(j + 1) % p_x.size]
                w_4 = distance_table[j % p_x.size][(i + 1) % p_x.size]
                if (w_1 + w_2) > (w_3 + w_4):
                    tmp_ix2 = p_x[(i + 1) % p_x.size]
                    tmp_iy2 = p_y[(i + 1) % p_x.size]
                    tmp_jx2 = p_x[(j + 1) % p_x.size]
                    tmp_jy2 = p_y[(j + 1) % p_x.size]
                    p_x[(i + 1) % p_x.size] = tmp_jx2
                    p_y[(i + 1) % p_x.size] = tmp_jy2
                    p_x[(j + 1) % p_x.size] = tmp_ix2
                    p_y[(j + 1) % p_x.size] = tmp_iy2
                    # swap i+1, j+1
                    tmp_row_ip1 = distance_table[(i + 1) % p_x.size]
                    distance_table[(i + 1) % p_x.size] = distance_table[
                        (j + 1) % p_x.size
                    ]
                    distance_table[(j + 1) % p_x.size] = tmp_row_ip1

                    tmp_col_ip1 = distance_table[:, (i + 1) % p_x.size]
                    distance_table[:][(i + 1) % p_x.size] = distance_table[:][
                        (j + 1) % p_x.size
                    ]
                    distance_table[:][(j + 1) % p_x.size] = tmp_col_ip1
                    count += 1
                    print("compare {} {} {} {} swapped".format(i, i + 1, j, j + 1))
                else:
                    print("compare {} {} {} {}".format(i, i + 1, j, j + 1))
                j += 1
        i += 1

        print("count={}".format(count))
        if count == 0:
            break

    total_after = 0.0
    i = 0
    while i < (p_x.size - 1):
        total_after += distance_table[i][i + 1]
        i += 1

    print("before={} -> after={}".format(total_before, total_after))

    plt.plot(p_x, p_y)  # "o"は小さい円(circle marker)
    plt.savefig("tsp_after.png")


if __name__ == "__main__":
    main()
