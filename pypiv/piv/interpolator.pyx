import numpy as np
cimport numpy as np

from libc.math cimport fabs, pow

cimport cython
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef cubic_interpolation(np.ndarray[np.double_t, ndim=2] posx,
                        np.ndarray[np.double_t, ndim=2] posy,
                        np.ndarray[np.double_t, ndim=2] frame):

    cdef np.ndarray[np.double_t, ndim=1] position = np.array([-2.5, -1.5, -0.5, 0.5, 1.5, 2.5])
    cdef np.ndarray[np.double_t, ndim=2] output = np.zeros_like(posx)
    cdef np.ndarray[np.double_t, ndim=2] M  = np.array([[-3.6,  2.8,  1. ,  1. ,  2.8, -3.6],
                                                        [ 4.2, -5.4,  0. ,  0. , -5.4,  4.2],
                                                        [-1.6,  3.2,  2.2,  2.2,  3.2, -1.6],
                                                        [ 0.2, -0.6,  1.2,  1.2, -0.6,  0.2]])
    cdef int i, j, k, l, ix, iy
    cdef float x, y, dx, dy, outsum

    for i in range(posx.shape[0]):
        for j in range(posx.shape[1]):
            if (posx[i,j] < 0) or (posx[i,j] > frame.shape[0]):
                output[i,j] = 0
            elif (posy[i,j] < 0) or (posy[i,j] > frame.shape[1]):
                output[i,j] = 0
            else:
                ix, iy = int(posx[i, j]) + 3, int(posy[i, j]) + 3
                dx, dy = posx[i, j] % 1, posy[i, j] % 1

                outsum = 0
                for k in range(6):
                    for l in range(6):
                        x = fabs(dx - position[k])
                        y = fabs(dy - position[l])
                        x = M[0,k] + x*M[1, k] + pow(x, 2)*M[2, k] + pow(x, 3)*M[3, k]
                        y = M[0,l] + y*M[1, l] + pow(y, 2)*M[2, l] + pow(y, 3)*M[3, l]
                        outsum += frame[ix+k-2, iy+l-2]*x*y
                output[i, j] = outsum
    return output





