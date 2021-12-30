#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
import math
import numpy as np
import matplotlib.pyplot as plt


def load_tsp_file(inFileName):
    nodeNum = 0
    x = None
    y = None
    labelNames = None

    pat_header = re.compile('^([A-Z_]*) *: *(.*) *$')
    pat_nodesect = re.compile('^(NODE_COORD_SECTION|EOF)$')
    pat_nodedata = re.compile('^ *([0-9]+) +([-.0-9]+) +([-.0-9]+) *$')

    inFile = open(inFileName, "r")
    for line_with_crlf in inFile:
        line = line_with_crlf.rstrip('rn')

        match_header = pat_header.match(line)
        match_nodesect = pat_nodesect.match(line)
        match_nodedata = pat_nodedata.match(line)

        if match_header:
            match_key = match_header.group(1)
            match_value = match_header.group(2)
            if match_key in "DIMENSION":
                nodeNum = int(match_value)
                print("nodeNum = {}".format(nodeNum))
        elif match_nodesect:
            if match_nodesect.group(1) == "NODE_COORD_SECTION":
                print(match_nodesect.group(1))
                x = np.empty(nodeNum, np.float32)
                y = np.empty(nodeNum, np.float32)
                labelNames = np.chararray(nodeNum, itemsize=3)
        elif match_nodedata:
            nodeId = int(match_nodedata.group(1))
            nodeX = float(match_nodedata.group(2))
            nodeY = float(match_nodedata.group(3))

            x[nodeId - 1] = nodeX
            y[nodeId - 1] = nodeY
            labelNames[nodeId - 1] = str(nodeId)

        else:
            print("no match: '{}'".format(line))

    inFile.close

    print("calc distance ...")
    distance_table = np.empty((nodeNum, nodeNum), np.float32)
    for i in range(nodeNum):
        for j in range(nodeNum):
            if i == j:
                distance_table[i][j] = 0
            else:
                dx = x[j] - x[i]
                dy = y[j] - y[i]
                distance_table[i][j] = math.sqrt(dx * dx + dy * dy)

    return nodeNum, x, y, labelNames, distance_table


if __name__ == "__main__":
    e1x = np.empty(2, np.float32)
    e1y = np.empty(2, np.float32)
    e2x = np.empty(2, np.float32)
    e2y = np.empty(2, np.float32)

    inFileName = sys.argv[1]
    nodeNum, x, y, labelNames, distance_table = load_tsp_file(inFileName)

    tour = np.empty(nodeNum, np.int16)
    for i in range(nodeNum):
        tour[i] = i

    plt.plot(x, y)  # "o"は小さい円(circle marker)
    for i in range(nodeNum):
        plt.annotate(labelNames[i], xy=(x[i], y[i]))
    plt.savefig('tsp_2opt_%03d.png' % (0))
    plt.clf()

    total_before = 0.
    i = 0
    while i < nodeNum:
        total_before += distance_table[i][(i + 1) % nodeNum]
        i += 1

    print("opt-2 ...")
    error = 0
    swap_count = 0
    while True:
        i = 0
        count = 0
        while i < nodeNum:
            j = i + 2
            while True:
                if (nodeNum - 1) < j:
                    break
                if (j + 1) % nodeNum == i % nodeNum:
                    break
                tour_i = tour[i % nodeNum]
                tour_j = tour[j % nodeNum]
                tour_i_next = tour[(i + 1) % nodeNum]
                tour_j_next = tour[(j + 1) % nodeNum]
                w1 = distance_table[tour_i][tour_i_next]
                w2 = distance_table[tour_j][tour_j_next]
                w3 = distance_table[tour_i][tour_j_next]
                w4 = distance_table[tour_j][tour_i_next]
                if (w1 + w2) > (w3 + w4):
                    count += 1
                    swap_count += 1
                    print("compare {}({} {}x{}) {}({} {}x{}) {}({} {}x{}) {}({} {}x{}) swapped: {} -> {}".format(
                        tour_i, labelNames[tour_i], x[tour_i], y[tour_i],
                        tour_i_next, labelNames[tour_i_next], x[tour_i_next], y[tour_i_next],
                        tour_j, labelNames[tour_j], x[tour_j], y[tour_j],
                        tour_j_next, labelNames[tour_j_next], x[tour_j_next], y[tour_j_next], w1 + w2, w3 + w4))

                    dx = x[tour_i_next] - x[tour_i]
                    dy = y[tour_i_next] - y[tour_i]
                    distance = math.sqrt(dx * dx + dy * dy)
                    print("p(i)-p(i+1): {}, dtable={}".format(distance, distance_table[tour_i_next][tour_i]))
                    dx = x[tour_j_next] - x[tour_j]
                    dy = y[tour_j_next] - y[tour_j]
                    distance = math.sqrt(dx * dx + dy * dy)
                    print("p(j)-p(j+1): {}, dtable={}".format(distance, distance_table[tour_j_next][tour_j]))
                    dx = x[tour_j_next] - x[tour_i]
                    dy = y[tour_j_next] - y[tour_i]
                    distance = math.sqrt(dx * dx + dy * dy)
                    print("p(i)-p(j+1): {}, dtable={}".format(distance, distance_table[tour_j_next][tour_i]))
                    dx = x[tour_i_next] - x[tour_j]
                    dy = y[tour_i_next] - y[tour_j]
                    distance = math.sqrt(dx * dx + dy * dy)
                    print("p(j)-p(i+1): {}, dtable={}".format(distance, distance_table[tour_i_next][tour_j]))

                    e1x[0] = x[tour_i]
                    e1y[0] = y[tour_i]
                    e1x[1] = x[tour_i_next]
                    e1y[1] = y[tour_i_next]
                    e2x[0] = x[tour_j]
                    e2y[0] = y[tour_j]
                    e2x[1] = x[tour_j_next]
                    e2y[1] = y[tour_j_next]
                    k = 0
                    total_work = 0.
                    while k < nodeNum:
                        total_work += distance_table[tour[k]][tour[(k + 1) % nodeNum]]
                        k += 1
                    if total_before < total_work:
                        print("PreCheck: ERROR: distance more longger...: {} -> {}".format(total_before, total_work))
                        error = 1

                    tour[(i + 1) % nodeNum] = tour_j_next
                    tour[(j + 1) % nodeNum] = tour_i_next

                    x2 = np.empty(nodeNum)
                    y2 = np.empty(nodeNum)
                    for i in range(nodeNum):
                        x2[i] = x[tour[i]]
                        y2[i] = y[tour[i]]
                    plt.plot(x2, y2)
                    plt.plot(e1x, e1y, ':')
                    plt.plot(e2x, e2y, '-.')
                    plt.plot(x[tour[i]], y[tour[i]], 'o')
                    plt.plot(x[tour_i_next], y[tour_i_next], 'p')
                    plt.plot(x[tour[j]], y[tour[j]], 'x')
                    plt.plot(x[tour_j_next], y[tour_j_next], '+')

                    for i in range(nodeNum):
                        plt.annotate(labelNames[i], xy=(x[tour[i]], y[tour[i]]))

                    plt.savefig('tsp_2opt_%03d.png' % (swap_count))
                    plt.clf()

                    k = 0
                    total_work = 0.
                    while k < nodeNum:
                        total_work += distance_table[tour[k]][tour[(k + 1) % nodeNum]]
                        k += 1
                    if total_before < total_work:
                        print("PostCheck: ERROR: distance more longger...: {} -> {}".format(total_before, total_work))
                        error = 1
                    break

                else:
                    tour_i = tour[i % nodeNum]
                    tour_i_next = tour[(i + 1) % nodeNum]
                    tour_j = tour[i % nodeNum]
                    tour_j_next = tour[(j + 1) % nodeNum]
                    print("compare {}({}) {}({}) {}({}) {}({})".format(
                        tour_i, labelNames[tour_i], tour_i_next, labelNames[tour_i_next],
                        tour_j, labelNames[tour_j], tour_j_next, labelNames[tour_j_next]))
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
    while i < nodeNum:
        total_after += distance_table[tour[i]][tour[(i + 1) % nodeNum]]
        i += 1

    print("before={} -> after={}".format(total_before, total_after))

    x2 = np.empty(nodeNum)
    y2 = np.empty(nodeNum)
    for i in range(nodeNum):
        x2[i] = x[tour[i]]
        y2[i] = y[tour[i]]

    plt.plot(x2, y2)
    plt.plot(e1x, e1y, ':')
    plt.plot(e2x, e2y, '-.')
    plt.savefig('tsp_2opt_after.png')
