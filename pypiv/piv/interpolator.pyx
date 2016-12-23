#compile with
# cython interpolator.pyx
# gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/usr/include/python2.7 -o interpolator.so interpolator.c

import numpy as np
cimport numpy as np
cimport cython

from libc.math cimport fabs, pow

@cython.boundscheck(False)
@cython.wraparound(False)
def cubic_interpolation(np.ndarray[np.double_t, ndim=2] posx, np.ndarray[np.double_t, ndim=2] posy,
                        np.ndarray[np.double_t, ndim=2] frame, np.ndarray[np.double_t, ndim=1] position,
                        np.ndarray[np.double_t, ndim=2] output, np.ndarray[np.double_t, ndim=2] M,
                        np.ndarray[np.double_t, ndim=1] x, np.ndarray[np.double_t, ndim=1] y):
    cdef int i, j, k, l, ix, iy
    cdef float dx, dy, outsum

    for i in range(posx.shape[0]):
        for j in range(posx.shape[1]):
            if (posx[i,j] < 0) or (posx[i,j] > frame.shape[0]) or (posy[i,j] < 0) or (posy[i,j] > frame.shape[1]):
                output[i, j] = 0
            else:
                ix, iy = <int>posx[i, j] + 3, <int>posy[i, j] + 3
                dx, dy = posx[i, j] % 1, posy[i, j] % 1

                outsum = 0
                for k in range(6):
                    x[k] = fabs(dx - position[k])
                    y[k] = fabs(dy - position[k])
                    x[k] = M[0,k] + x[k]*M[1, k] + pow(x[k], 2)*M[2, k] + pow(x[k], 3)*M[3, k]
                    y[k] = M[0,k] + y[k]*M[1, k] + pow(y[k], 2)*M[2, k] + pow(y[k], 3)*M[3, k]
                for k in range(6):
                    for l in range(6):
                        outsum += frame[ix+k-2, iy+l-2]*x[k]*y[l]

                output[i, j] = outsum




