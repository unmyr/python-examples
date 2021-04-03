# -*- coding: utf-8 -*-
"""Save plot"""
import numpy as np
import matplotlib.pyplot as plt


x = np.arange(-10.0, 10.0, 0.1)
y = np.sin(x)
plt.plot(x, y)
plt.savefig('matplotlib_plot_sin.png')
