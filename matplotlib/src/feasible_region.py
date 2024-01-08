# -*- coding: utf-8 -*-
"""Plot feasible region."""
import matplotlib.pyplot as plt
import numpy as np


def main():
    """Run main."""
    # plot the feasible region
    x_min = -10
    x_max = 100
    y_min = -10
    y_max = 100
    mesh_x1, mesh_x2 = np.meshgrid(np.linspace(x_min, x_max, 300), np.linspace(y_min, y_max, 300))

    fig = plt.figure(figsize=(12, 8))

    ax = fig.add_subplot(1, 1, 1)  # Create one plot area.
    ax.set_title("LP")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    ax.imshow(
        (
            (mesh_x1 >= 0)
            & (mesh_x2 >= 0)
            & (mesh_x1 + 2 * mesh_x2 <= 80)
            & (4 * mesh_x1 + 4 * mesh_x2 <= 180)
            & (3 * mesh_x1 + mesh_x2 <= 90)
        ).astype(int)
        * (5 * mesh_x1 + 4 * mesh_x2),
        extent=(mesh_x1.min(), mesh_x1.max(), mesh_x2.min(), mesh_x2.max()),
        origin="lower",
        cmap="Blues",
        alpha=0.8,
    )

    # plot the lines defining the constraints
    x1 = np.linspace(x_min, x_max, 2000)
    # y >= 0
    y1 = x1 * 0
    # x_1 + 2 x_2 <= 80
    y2 = (80 - x1) / 2.0
    # 4 x_1 + 4 x_2 <= 180
    y3 = (180 - 4 * x1) / 4.0
    # 3 x_1 + x_2 <= 90
    y4 = 90 - 3 * x1

    # 0 <= x
    x0 = np.zeros(2000)
    y0 = np.linspace(y_min, y_max, 2000)

    # Make plot
    plt.plot(x0, y0, label=r"$x=0$")
    plt.plot(x1, y1, label=r"$y=0$")
    plt.plot(x1, y2, label=r"$x_1 + 2 x_2 \leq 80$")
    plt.plot(x1, y3, label=r"$4 x_1 + 4 x_2 \leq 180$")
    plt.plot(x1, y4, label=r"$3 x_1 + x_2 \leq 90$")

    plt.legend()

    fig.tight_layout()
    fig.show()
    fig.savefig("feasible_region.png")


if __name__ == "__main__":
    main()

# EOF
