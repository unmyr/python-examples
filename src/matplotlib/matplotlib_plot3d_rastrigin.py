#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Plot rastrigin function."""
from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-5.12, 5.12, 100)
y = np.linspace(-5.12, 5.12, 100)
x, y = np.meshgrid(x, y)
z = 20 + x**2 - 10 * np.cos(2 * np.pi * x) + y**2 - 10 * np.cos(2 * np.pi * y)

figure = plt.figure()
axe = figure.add_subplot(111, projection='3d')
surface = axe.plot_surface(
    x, y, z,
    rstride=1, cstride=1,
    cmap=cm.winter, linewidth=0, antialiased=False
)

# figure.savefig("matplotlib_plot3d_rastrigin.png")
plt.show()
