import numba as nb
import numpy as np


@nb.njit(fastmath=True)
def norm(l):
    s = 0.
    for i in range(l.shape[0]):
        s += l[i]**2
    return np.sqrt(s)

def normalize(vector):
    return vector / norm(vector)

def reflected(vector, axis):
    return vector - 2 * np.dot(vector, axis) * axis