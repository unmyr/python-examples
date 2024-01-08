# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
"""nop example."""
from __future__ import print_function
import math
import numpy

import matplotlib.cm
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot  # noqa: E402


def func_d1(p_x):
    """Euclidean distance."""
    return numpy.sqrt(p_x[1:] * p_x[1:] + p_x[:-1] * p_x[:-1])


def func_d2(p_x):
    """func z."""
    return numpy.absolute(p_x[1:]) * numpy.absolute(p_x[:-1])


def func_d3(p_x):
    """func z."""
    return numpy.absolute(p_x[1:]) + numpy.absolute(p_x[:-1])


def main():
    """main."""
    levels = [-math.sqrt(2), -1, -0.5, 0, 0.5, 1, math.sqrt(2)]

    delta = 0.025
    x_seq = numpy.arange(-2.0, 2.0, delta)
    y_seq = numpy.arange(-2.0, 2.0, delta)
    grid_x, grid_y = numpy.meshgrid(x_seq, y_seq)

    fig = matplotlib.pyplot.figure(1, (9.0, 2 * 6.0))
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)

    p_z = func_d1(numpy.vstack([grid_x.ravel(), grid_y.ravel()])).reshape(len(x_seq), len(y_seq))
    ax1.set_aspect("equal")
    cs_plot = ax1.contour(grid_x, grid_y, p_z, levels)
    color_bar = fig.colorbar(cs_plot, cax=matplotlib.pyplot.axes([0.85, 0.1, 0.075, 0.8]))
    color_bar.ax.set_ylabel("verbosity coefficient")
    ax1.clabel(cs_plot, inline=1, fontsize=10)
    # ax1.title('f(x,y) = |x| + |y|')
    # matplotlib.pyplot.savefig('matplotlib_plot_contour_1.png')

    p_z = func_d2(numpy.vstack([grid_x.ravel(), grid_y.ravel()])).reshape(len(x_seq), len(y_seq))
    ax2.set_aspect("equal")
    cs_plot = ax2.contour(grid_x, grid_y, p_z, levels)
    ax2.clabel(cs_plot, inline=1, fontsize=10)
    color_bar = matplotlib.pyplot.colorbar(cs_plot, cax=ax2)
    color_bar.ax.set_ylabel("verbosity coefficient")
    # ax2.title('f(x,y) = |x| + |y|')
    matplotlib.pyplot.savefig("matplotlib_plot_contour_2.png")

    # pylint: disable=pointless-string-statement
    """
    z = func_d3(
        numpy.vstack([grid_x.ravel(), grid_y.ravel()])
    ).reshape(len(x_seq), len(y_seq))
    matplotlib.pyplot.gca().set_aspect('equal', adjustable='box')
    levels = [-math.sqrt(2), -1, -0.5, 0, 0.5, 1, math.sqrt(2)]
    cs_plot = matplotlib.pyplot.contour(grid_x, grid_y, z, levels)
    matplotlib.pyplot.clabel(cs_plot, inline=1, fontsize=10)
    color_bar = matplotlib.pyplot.colorbar(cs_plot)
    color_bar.ax.set_ylabel('verbosity coefficient')
    matplotlib.pyplot.title('f(x,y) = |x| + |y|')
    matplotlib.pyplot.savefig('matplotlib_plot_contour_3.png')
    """


if __name__ == "__main__":
    main()

# EOF
