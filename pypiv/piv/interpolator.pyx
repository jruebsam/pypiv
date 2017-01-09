#compile with
# cython interpolator.pyx
# gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/usr/include/python2.7 -o interpolator.so interpolator.c

import numpy as np
cimport numpy as np
cimport cython

from libc.math cimport fabs, pow

@cython.boundscheck(False)
@cython.wraparound(False)
def cubic_interpolation(
    np.ndarray[np.double_t, ndim=1] posx,
    np.ndarray[np.double_t, ndim=1] posy,
    np.ndarray[np.double_t, ndim=2] frame, int lx, int ly):

    cdef np.ndarray[np.double_t, ndim=1] x = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    cdef np.ndarray[np.double_t, ndim=1] y = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

    cdef np.ndarray[np.double_t, ndim=1] position = np.array([-2.5, -1.5,  -0.5, 0.5,  1.5,  2.5])

    cdef np.ndarray[np.double_t, ndim=2] M   =     np.array([[-3.6,  2.8,   1.0, 1.0,  2.8, -3.6],
                                                             [ 4.2, -5.4,   0.0, 0.0, -5.4,  4.2],
                                                             [-1.6,  3.2,  -2.2, -2.2,  3.2, -1.6],
                                                             [ 0.2, -0.6,   1.2, 1.2, -0.6,  0.2]])
    cdef np.ndarray[np.double_t, ndim=1] output = np.zeros_like(posx)
    cdef int i, k, l, ix, iy
    cdef float dx, dy, outsum

    for i in range(posx.shape[0]):
        if (posx[i] < 0) or (posx[i] > lx) or (posy[i] < 0) or (posy[i] > ly):
            output[i] = 0
        else:
            ix, iy = <int>posx[i] + 3, <int>posy[i] + 3
            dx, dy = posx[i] % 1, posy[i] % 1
            outsum = 0
            for k in range(6):
                x[k] = fabs(dx - position[k])
                y[k] = fabs(dy - position[k])
                x[k] = M[0,k] + x[k]*M[1, k] + pow(x[k], 2)*M[2, k] + pow(x[k], 3)*M[3, k]
                y[k] = M[0,k] + y[k]*M[1, k] + pow(y[k], 2)*M[2, k] + pow(y[k], 3)*M[3, k]
            for k in range(6):
                for l in range(6):
                    outsum += frame[ix+k-2, iy+l-2]*x[k]*y[l]
            output[i] = outsum
    return output



