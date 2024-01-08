# -*- coding: utf-8 -*-
"""Plot a graph with animation."""
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()
(line,) = ax.plot([], [], lw=2)
ax.grid()
x_data, y_data = [], []


def data_gen(t=0):
    """Generate data."""
    cnt = 0
    while cnt < 1000:
        cnt += 1
        t += 0.1
        yield t, np.sin(2 * np.pi * t) * np.exp(-t / 10.0)


def init():
    """Initialize plot settings."""
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlim(0, 10)
    del x_data[:]
    del y_data[:]
    line.set_data(x_data, y_data)
    return (line,)


def update(data):
    """Update plot data."""
    t, y = data
    x_data.append(t)
    y_data.append(y)
    x_min, x_max = ax.get_xlim()

    if t >= x_max:
        ax.set_xlim(x_min, 2 * x_max)
        ax.figure.canvas.draw()
    line.set_data(x_data, y_data)

    return (line,)


if __name__ == "__main__":
    ani = animation.FuncAnimation(
        fig, update, data_gen, blit=False, interval=10, repeat=False, init_func=init
    )
    plt.show()
