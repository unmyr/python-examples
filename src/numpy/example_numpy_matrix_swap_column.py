"""Show examples of `np.array` and `np.copy`."""
import numpy as np

mat = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]], np.int16)
print(mat)

tmp_mat_col1 = np.copy(mat[:, 1])
mat[:, 1] = mat[:, 2]
mat[:, 2] = tmp_mat_col1
print(mat)
