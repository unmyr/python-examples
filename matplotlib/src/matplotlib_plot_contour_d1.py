# -*- coding: utf-8 -*-
"""Plot Euclidean distance function."""
import math
import numpy

import matplotlib.cm
import matplotlib.patches
import matplotlib.transforms
import matplotlib
matplotlib.use('Agg')
# pylint: disable=wrong-import-position
import matplotlib.pyplot  # noqa: E402


def func_d1(p_x):
    """Euclidean distance."""
    return numpy.sqrt(p_x[1:] * p_x[1:] + p_x[:-1] * p_x[:-1])


def main():
    """main."""
    levels = [
        0, 0.25, 0.5, 1 / math.sqrt(2), 1, math.sqrt(2)
    ]

    delta = 0.025
    x_seq = numpy.arange(-2.0, 2.0, delta)
    y_seq = numpy.arange(-2.0, 2.0, delta)
    grid_x, grid_y = numpy.meshgrid(x_seq, y_seq)

    # Get Current Axis
    ax = matplotlib.pyplot.gca()

    # draw rectangles
    t_start = ax.transData
    t = matplotlib.transforms.Affine2D().rotate_deg_around(0, 0, 45)
    t_end = t + t_start
    w = math.sqrt(2)
    square_1 = matplotlib.pyplot.Rectangle(
        (-w / 2., -w / 2.), w, w, facecolor='none', edgecolor='#6666ff',
        linewidth=1.0, linestyle='dashed', transform=t_end,
        label='|x|+|y|'
    )
    w = 2.
    square_2 = matplotlib.pyplot.Rectangle(
        (-w / 2., -w / 2.), w, w, facecolor='none', edgecolor='#66ff66',
        linewidth=1.0, linestyle='dashed', transform=t_end,
        label='|x|+|y|'
    )

    z = func_d1(
        numpy.vstack([grid_x.ravel(), grid_y.ravel()])
    ).reshape(len(x_seq), len(y_seq))
    ax.set_aspect('equal', adjustable='box')
    cs_plot = matplotlib.pyplot.contour(
        grid_x, grid_y, z, levels,
        cmap='Dark2'
    )
    matplotlib.pyplot.clabel(cs_plot, inline=1, fontsize=10)
    color_bar = matplotlib.pyplot.colorbar(cs_plot)
    color_bar.ax.set_ylabel('verbosity coefficient')
    matplotlib.pyplot.title(r'$f(x,y) = \sqrt{x^2 + y^2}$')
    ax.add_patch(square_1)
    ax.add_patch(square_2)
    ax.legend(
        [square_1, square_2],
        [
            r'A square with side length $\sqrt{2}$',
            'A square with side length 2'
        ]
    )
    matplotlib.pyplot.savefig('matplotlib_plot_contour_d1.png')
    # matplotlib.pyplot.show()


if __name__ == '__main__':
    main()

# EOF
