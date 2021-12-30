#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Load TSP file."""
import sys
import re
import math
import numpy as np
import matplotlib.pyplot as plt


def load_tsp_file(in_filename):
    """Load TSP file."""
    node_num = 0
    # p_x = None
    # p_y = None
    # label_names = None

    pat_header = re.compile('^([A-Z_]*) *: *(.*) *$')
    pat_nodesect = re.compile('^(NODE_COORD_SECTION|EOF)$')
    pat_nodedata = re.compile('^ *([0-9]+) +([-.0-9]+) +([-.0-9]+) *$')

    in_file_handle = open(in_filename, "r")
    for line_with_crlf in in_file_handle:
        line = line_with_crlf.rstrip('rn')

        match_header = pat_header.match(line)
        match_nodesect = pat_nodesect.match(line)
        match_nodedata = pat_nodedata.match(line)

        if match_header:
            match_key = match_header.group(1)
            match_value = match_header.group(2)
            if match_key in "DIMENSION":
                node_num = int(match_value)
                print("node_num = {}".format(node_num))
        elif match_nodesect:
            if match_nodesect.group(1) == "NODE_COORD_SECTION":
                print(match_nodesect.group(1))
                p_x = np.empty(node_num, np.float32)
                p_y = np.empty(node_num, np.float32)
                label_names = np.chararray(node_num, itemsize=3)
        elif match_nodedata:
            node_id = int(match_nodedata.group(1))
            node_x = float(match_nodedata.group(2))
            node_y = float(match_nodedata.group(3))

            p_x[node_id - 1] = node_x
            p_y[node_id - 1] = node_y
            label_names[node_id - 1] = str(node_id)

        else:
            print("no match: '{}'".format(line))

    in_file_handle.close()

    print("calc distance ...")
    distance_table = np.empty((node_num, node_num), np.float32)
    for i in range(node_num):
        for j in range(node_num):
            if i == j:
                distance_table[i][j] = 0
            else:
                d_x = p_x[j] - p_x[i]
                d_y = p_y[j] - p_y[i]
                distance_table[i][j] = math.sqrt(d_x * d_x + d_y * d_y)

    return node_num, p_x, p_y, label_names, distance_table


def main():
    """Run main."""
    in_filename = sys.argv[1]
    node_num, p_x, p_y, label_names, distance_table = load_tsp_file(in_filename)

    tour = np.empty(node_num, np.int16)
    for i in range(node_num):
        tour[i] = i

    plt.plot(p_x, p_y)  # "o"は小さい円(circle marker)
    for i in range(node_num):
        plt.annotate(label_names[i], xy=(p_x[i], p_y[i]))
    plt.savefig('tsp_2opt_%03d.png' % (0))
    plt.clf()

    total_before = 0.
    i = 0
    while i < node_num:
        total_before += distance_table[i][(i + 1) % node_num]
        i += 1

    print("opt-2 ...")
    error = 0
    swap_count = 0
    while True:
        i = 0
        count = 0
        while i < node_num:
            j = i + 2
            while True:
                if (node_num - 1) < j:
                    break
                if (j + 1) % node_num == i % node_num:
                    break
                tour_i = tour[i % node_num]
                tour_j = tour[j % node_num]
                tour_i_next = tour[(i + 1) % node_num]
                tour_j_next = tour[(j + 1) % node_num]
                w_1 = distance_table[tour_i][tour_i_next]
                w_2 = distance_table[tour_j][tour_j_next]
                w_3 = distance_table[tour_i][tour_j]
                w_4 = distance_table[tour_j_next][tour_i_next]
                if (w_1 + w_2) > (w_3 + w_4):
                    count += 1
                    swap_count += 1
                    print("compare {}({} {}x{}) {}({} {}x{}) {}({} {}x{}) {}({} {}x{}) swapped: {} -> {}".format(
                        tour_i, label_names[tour_i], p_x[tour_i], p_y[tour_i],
                        tour_i_next, label_names[tour_i_next], p_x[tour_i_next], p_y[tour_i_next],
                        tour_j, label_names[tour_j], p_x[tour_j], p_y[tour_j],
                        tour_j_next, label_names[tour_j_next], p_x[tour_j_next], p_y[tour_j_next],
                        w_1 + w_2, w_3 + w_4))

                    d_x = p_x[tour_i_next] - p_x[tour_i]
                    d_y = p_y[tour_i_next] - p_y[tour_i]
                    distance = math.sqrt(d_x * d_x + d_y * d_y)
                    print("p(i)-p(i+1): {}, dtable={}".format(
                        distance, distance_table[tour_i_next][tour_i]))
                    d_x = p_x[tour_j_next] - p_x[tour_j]
                    d_y = p_y[tour_j_next] - p_y[tour_j]
                    distance = math.sqrt(d_x * d_x + d_y * d_y)
                    print("p(j)-p(j+1): {}, dtable={}".format(
                        distance, distance_table[tour_j_next][tour_j]))
                    d_x = p_x[tour_j_next] - p_x[tour_i]
                    d_y = p_y[tour_j_next] - p_y[tour_i]
                    distance = math.sqrt(d_x * d_x + d_y * d_y)
                    print("p(i)-p(j+1): {}, dtable={}".format(
                        distance, distance_table[tour_j_next][tour_i]))
                    d_x = p_x[tour_i_next] - p_x[tour_j]
                    d_y = p_y[tour_i_next] - p_y[tour_j]
                    distance = math.sqrt(d_x * d_x + d_y * d_y)
                    print("p(j)-p(i+1): {}, dtable={}".format(
                        distance, distance_table[tour_i_next][tour_j]))

                    k = 0
                    total_work = 0.
                    while k < node_num:
                        total_work += distance_table[tour[k]][tour[(k + 1) % node_num]]
                        k += 1
                    if total_before < total_work:
                        print("PreCheck: ERROR: distance more longger...: {} -> {}".format(
                            total_before, total_work))
                        error = 1

                    sub_path = np.empty(j - i, np.int16)
                    k = 0
                    for k in range(j - i):
                        sub_path[k] = tour[(j - k) % node_num]
                    k = 0
                    for k in range(sub_path.size):
                        tour[(i + 1 + k) % node_num] = sub_path[k]

                    p_x2 = np.empty(node_num)
                    p_y2 = np.empty(node_num)
                    for i in range(node_num):
                        p_x2[i] = p_x[tour[i]]
                        p_y2[i] = p_y[tour[i]]
                    plt.plot(p_x2, p_y2)
                    plt.plot(p_x[tour[i]], p_y[tour[i]], 'o')
                    plt.plot(p_x[tour_i_next], p_y[tour_i_next], 'p')
                    plt.plot(p_x[tour[j]], p_y[tour[j]], 'x')
                    plt.plot(p_x[tour_j_next], p_y[tour_j_next], '+')

                    for i in range(node_num):
                        plt.annotate(label_names[i], xy=(p_x[tour[i]], p_y[tour[i]]))

                    plt.savefig('tsp_2opt_%03d.png' % (swap_count))
                    plt.clf()

                    k = 0
                    total_work = 0.
                    while k < node_num:
                        total_work += distance_table[tour[k]][tour[(k + 1) % node_num]]
                        k += 1
                    if total_before < total_work:
                        print("PostCheck: ERROR: distance more longger...: {} -> {}".format(
                            total_before, total_work))
                        error = 1
                        break

                else:
                    tour_i = tour[i % node_num]
                    tour_i_next = tour[(i + 1) % node_num]
                    tour_j = tour[i % node_num]
                    tour_j_next = tour[(j + 1) % node_num]
                    print("compare {}({}) {}({}) {}({}) {}({})".format(
                        tour_i, label_names[tour_i], tour_i_next, label_names[tour_i_next],
                        tour_j, label_names[tour_j], tour_j_next, label_names[tour_j_next]))
                j += 1
            if error == 1:
                break
            i += 1

        print("count={}".format(count))
        if error == 1:
            print("error detected.")
            break
        if count == 0:
            break

    total_after = 0.
    i = 0
    while i < node_num:
        total_after += distance_table[tour[i]][tour[(i + 1) % node_num]]
        i += 1

    print("before={} -> after={}".format(total_before, total_after))

    p_x2 = np.empty(node_num)
    p_y2 = np.empty(node_num)
    for i in range(node_num):
        p_x2[i] = p_x[tour[i]]
        p_y2[i] = p_y[tour[i]]

    plt.plot(p_x2, p_y2)
    plt.savefig('tsp_2opt_after.png')


if __name__ == '__main__':
    main()
