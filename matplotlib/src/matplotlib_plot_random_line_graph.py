#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

x = np.random.randn(30)
y = np.sin(x) + np.random.randn(30)
# plt.plot(x, y, "o")  # "o"は小さい円(circle marker)
plt.plot(x, y)  # "o"は小さい円(circle marker)
# plt.show()
plt.savefig("matplotlib_plot_random_line_graph.png")
