"""Show examples of `np.empty`, `np.zeros`, `np.ones` and `np.dandom`."""
import numpy as np

if __name__ == '__main__':
    vec_empty = np.empty(3)
    print("vec_empty(size:{}, ndim:{}, shape:{}, dtype:{}):\n{}".format(
        vec_empty.size, vec_empty.ndim, vec_empty.shape, vec_empty.dtype,
        vec_empty))

    vec_zeros = np.zeros(3)
    print("vec_zeros(size:{}, ndim:{}, shape:{}, dtype:{}):\n{}".format(
        vec_zeros.size, vec_zeros.ndim, vec_zeros.shape, vec_zeros.dtype,
        vec_zeros))

    vec_ones = np.ones(3)
    print("vec_ones(size:{}, ndim:{}, shape:{}, dtype:{}):\n{}".format(
        vec_ones.size, vec_ones.ndim, vec_ones.shape, vec_ones.dtype,
        vec_ones))

    vec_rand = np.random.randint(0, 10, (3), dtype=np.int16)
    print("vec_rand(size:{}, ndim:{}, shape:{}, dtype:{}):\n{}".format(
        vec_rand.size, vec_rand.ndim, vec_rand.shape, vec_rand.dtype,
        vec_rand))
