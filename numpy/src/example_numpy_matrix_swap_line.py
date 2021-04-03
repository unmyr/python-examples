"""Show examples of `np.array` and `np.copy`."""
import numpy as np

if __name__ == "__main__":
    mat = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]], np.int16)
    print(mat)

    tmp_mat1 = np.copy(mat[1])
    mat[1] = mat[2]
    mat[2] = tmp_mat1
    print(mat)
