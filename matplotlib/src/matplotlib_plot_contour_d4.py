# -*- coding: utf-8 -*-
"""Plot distance function."""
import math
import numpy

import matplotlib.cm
import matplotlib
matplotlib.use('Agg')
# pylint: disable=wrong-import-position
import matplotlib.pyplot


def func_d4(p_x):
    """Func d1 + d2."""
    return numpy.sqrt(
        p_x[1:]*p_x[1:] + p_x[:-1]*p_x[:-1]
        + 2 * numpy.absolute(p_x[1:]) * numpy.absolute(p_x[:-1])
    )


def main():
    """main."""
    levels = [0, 0.25, 0.5, 1, math.sqrt(2), 2, 3]

    delta = 0.00625
    x_seq = numpy.arange(-2.0, 2.0, delta)
    y_seq = numpy.arange(-2.0, 2.0, delta)
    grid_x, grid_y = numpy.meshgrid(x_seq, y_seq)

    # Get Current Axis
    ax = matplotlib.pyplot.gca()

    # draw circle.
    circle_r1 = matplotlib.pyplot.Circle(
        (0, 0), 1, facecolor='none', edgecolor='#ff6666',
        linewidth=1.0, linestyle='dashed', label='r=1.0'
    )

    circle_r0 = matplotlib.pyplot.Circle(
        (0, 0), math.sqrt(2)/2, facecolor='none', edgecolor='#cccc44',
        linewidth=1.0, linestyle='dashed'
    )

    z = func_d4(
        numpy.vstack([grid_x.ravel(), grid_y.ravel()])
    ).reshape(len(x_seq), len(y_seq))
    ax.set_aspect('equal', adjustable='box')
    cs_plot = matplotlib.pyplot.contour(
        grid_x, grid_y, z, levels,
        cmap=matplotlib.pyplot.cm.Dark2
    )
    matplotlib.pyplot.clabel(cs_plot, inline=1, fontsize=10)
    cbar = matplotlib.pyplot.colorbar(cs_plot)
    cbar.ax.set_ylabel('verbosity coefficient')
    matplotlib.pyplot.title('f(x,y) = sqrt(2*|x|*|y| + x*x + y*y)')
    ax.add_patch(circle_r0)
    ax.add_patch(circle_r1)
    ax.legend(
        [circle_r0, circle_r1],
        ['circle r=1/sqrt(2)', 'circle r=1.0'])
    matplotlib.pyplot.savefig('matplotlib_plot_contour_d4.png')


if __name__ == '__main__':
    main()

# EOF