"""Show examples of `np.dandom`."""
import numpy as np

if __name__ == '__main__':
    data = np.random.randint(4, size=10)
    print(data)

    data = np.random.randint(-1, 2, (10, 2)).astype("float32")
    print("randint:", data)

    x_data = np.random.rand(5, 2, 1)  # .astype("float32")
    print(x_data)
    for elem in x_data:
        if elem[0] < 0.5:
            print("%.2f < 0.5,%.2f" % (elem[0], elem[1]))
        else:
            print("%.2f > 0.5,%.2f" % (elem[0], elem[1]))
