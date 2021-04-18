# -*- coding: utf-8 -*-
"""Place a legend inside of plot area."""
import matplotlib.pyplot as plt
import numpy as np


def main():
    """Run main."""
    x = np.arange(-0.2, 2.2, 0.1)

    fig = plt.figure(figsize=(6, 4))

    ax = fig.add_subplot(1, 1, 1)  # Create one plot area.
    ax.set_title('A linear function')
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.set_aspect('equal', adjustable='box')

    ax.plot(x, x * 1, label=r'$y=x$')
    ax.plot(x, x * 2, label=r'$y=2x$')
    ax.plot(x, x * 3, label=r'$y=3x$')
    ax.plot(x, x * 4, label=r'$y=4x$')
    ax.plot(x, x * 5, label=r'$y=5x$')
    ax.plot(x, x * 6, label=r'$y=6x$')
    ax.plot(x, x * 7, label=r'$y=7x$')
    ax.plot(x, x * 8, label=r'$y=8x$')
    ax.plot(x, x * 9, label=r'$y=9x$')
    ax.legend(
        loc='lower right', ncol=2
    )

    fig.tight_layout()
    fig.show()


if __name__ == '__main__':
    main()

# EOF
