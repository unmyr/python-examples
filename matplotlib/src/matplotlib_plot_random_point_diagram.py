#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

x = np.random.randn(30)
y = np.sin(x) + np.random.randn(30)
plt.plot(x, y, "o")  # "o"は小さい円(circle marker)
plt.savefig("matplotlib_plot_random_point_diagram.png")
