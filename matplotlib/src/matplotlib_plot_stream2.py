import numpy as np
import matplotlib.pyplot as plt

# Data
x = np.linspace(-10, 10, 10)
y = np.linspace(-10, 10, 10)
X, Y = np.meshgrid(x, y)
U = X * 0 + 1
V = X * 0
start_points = [[0, 0]]

# Base streamline plot
plt.figure()
sp1 = plt.streamplot(x, y, U, V, color=[.5] * 3)

# Streamline plot with 'start_points' argument
sp2 = plt.streamplot(x, y, U, V, start_points=start_points,
                     color='r')
plt.plot(*start_points[0], marker='o', label="Starting point")
plt.plot([], [], color='r', label="Associated streamline")

# Legend and limits
plt.xlim(-10, 10)
plt.ylim(-10, 10)
plt.legend(numpoints=1)

plt.show()
