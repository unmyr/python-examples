#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate TSP"""
import os
import datetime
import numpy as np

script_basename = os.path.splitext(os.path.basename(__file__))[0]


def main(data_num):
    """Run main."""
    datetime_str = datetime.date.today().strftime("%Y%m%d")
    tsp_name = "random_n{}_{}".format(data_num, datetime_str)
    out_filename = "{}.tsp".format(tsp_name)

    out_file_handle = open(out_filename, "w")
    header_of_file = """NAME : {name}
COMMENT : {comment}
TYPE : TSP
DIMENSION: {dim}
EDGE_WEIGHT_TYPE : EUC_2D
NODE_COORD_SECTION
""".format(name=tsp_name, comment="Random Generate", dim=data_num)

    out_file_handle.write(str(header_of_file))

    p_x = np.random.randn(data_num)
    p_y = np.sin(p_x) + np.random.randn(p_x.size)

    for i in range(0, data_num):
        out_file_handle.write("%3d %5.2f %5.2f\n" % (i + 1, p_x[i], p_y[i]))
    out_file_handle.write("EOF\n")
    out_file_handle.close()


if __name__ == '__main__':
    DATA_NUM = 30
    main(DATA_NUM)
