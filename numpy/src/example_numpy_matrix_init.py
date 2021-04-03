"""Initialize matrix."""
import numpy as np

mat_empty = np.empty((4, 3), np.int16)
print("mat_empty(size:{}, ndim:{}, shape:{}, dtype:{}):\n{}".format(
    mat_empty.size,
    mat_empty.ndim,
    mat_empty.shape,
    mat_empty.dtype,
    mat_empty))
print(mat_empty.strides)
print(mat_empty.shape[0])

mat_zeros = np.zeros((3, 4))
print("mat_zeros(size:{}, ndim:{}, shape:{}, dtype:{}):\n{}".format(
    mat_zeros.size,
    mat_zeros.ndim,
    mat_zeros.shape,
    mat_zeros.dtype,
    mat_zeros))

mat_ones = np.ones((3, 4), np.int16)
print("mat_ones(size:{}, ndim:{}, shape:{}, dtype:{}):\n{}".format(
    mat_ones.size, mat_ones.ndim, mat_ones.shape, mat_ones.dtype, mat_ones))

mat_rand = np.random.randint(0, 10, (4, 3), np.int16)
print("mat_rand(size:{}, ndim:{}, shape:{}, dtype:{}):\n{}".format(
    mat_rand.size, mat_rand.ndim, mat_rand.shape, mat_rand.dtype, mat_rand))
