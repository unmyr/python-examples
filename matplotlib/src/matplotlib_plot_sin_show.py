# -*- coding: utf-8 -*-
"""Plot of Sine"""
import math

import matplotlib.pyplot as plt
import numpy as np


def main():
    """Run main."""
    x = np.arange(-math.pi, math.pi, 0.2)
    y1 = np.sin(x)
    y2 = np.cos(x)

    fig = plt.figure(figsize=(6, 4))

    ax = fig.add_subplot(1, 1, 1)  # Create one plot area.
    ax.set_title("Sine wave")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")

    ax.plot(x, y1, label=r"$\sin(x)$")
    ax.plot(x, y2, label=r"$\cos(x)$")
    ax.legend()

    fig.savefig("matplotlib_plot_sin.png")

    fig.tight_layout()
    fig.show()


if __name__ == "__main__":
    main()

# EOF
