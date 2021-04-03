#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Parse the tsp file using a regular expression."""

import re

if __name__ == "__main__":
    pat = re.compile('^([A-Z_]*) *: *(.*) *$')
    pat_nodesect = re.compile('^(NODE_COORD_SECTION|EOF)$')
    pat_nodedata = re.compile('^ *([0-9]+) +([0-9]+) +([0-9]+) *$')

    texts = (
        "NAME : a280",
        "COMMENT : drilling problem (Ludwig)",
        "TYPE : TSP",
        "DIMENSION: 280",
        "EDGE_WEIGHT_TYPE : EUC_2D",
        "NODE_COORD_SECTION",
        "NODE_COORD_SECTION ",
        "  1 288 149",
        "280 280 133",
        "EOF"
    )

    for line in texts:
        match_header = pat.match(line)
        match_nodesect = pat_nodesect.match(line)
        match_nodedata = pat_nodedata.match(line)
        if match_header:
            print(match_header.groups())
        elif line in ("NODE_COORD_SECTION", "EOF"):
            print("match: {}".format(line))
        elif match_nodesect:
            print(match_nodesect.groups())
        elif match_nodedata:
            print(match_nodedata.groups())
        else:
            print("no match: '{}'".format(line))

# EOF
