# compile with
# cython interpolator.pyx
# gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/usr/include/python2.7 -o interpolator.so interpolator.c

import numpy as np
cimport numpy as np
cimport cython
from libc.math cimport fabs, pow

class CubicInterpolator(object):
    """
    Interpolator Class for the window deformation

    This class initializes and performs the interpolation.
    """

    def __init__(self, frame, window_size):
        """
        Initialization of the interpolator.

        **__init__(frame, window_size)**

        The cubic interpolation is performed in compiled c code,
        therefore the memory for right hand side and left hand side
        must be allocated and initialized for the matrix.
        The output is allocated as well.

        :param frame: image that is deformed
        :param window_size: size of the interrogation window over which is interpolated
        """
        self._frame = np.pad(frame, (3, 3), mode='constant')
        self._lx, self._ly = frame.shape
        self._ws = window_size

        self._x = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self._y = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

        self._M = np.array([[-3.6,  2.8,   1.0, 1.0,  2.8, -3.6],
                            [ 4.2, -5.4,   0.0, 0.0, -5.4,  4.2],
                            [-1.6,  3.2,  -2.2, -2.2,  3.2, -1.6],
                            [ 0.2, -0.6,   1.2, 1.2, -0.6,  0.2]])

        self._output = np.zeros((window_size, window_size))

    def interpolate(self, posx, posy):
        """
        Method to perform cubic interpolation of the deformed grid.

        **interpolate(posx, posy)**

        :param ndarray posx: moved x position of the deformed grid
        :param ndarray posy: moved y position of the deformed grid
        :returns: ndarray with interpolated sub image shaped to the original shape
        """
        output = cubic_interpolation(posx, posy, self._x, self._y, self._M,
                                     self._output.ravel(), self._frame, self._lx, self._ly)
        return output.reshape(self._ws, self._ws)

@cython.boundscheck(False)
@cython.wraparound(False)
def cubic_interpolation(np.ndarray[np.double_t, ndim=1] posx,
                        np.ndarray[np.double_t, ndim=1] posy,
                        np.ndarray[np.double_t, ndim=1] x,
                        np.ndarray[np.double_t, ndim=1] y,
                        np.ndarray[np.double_t, ndim=2] M,
                        np.ndarray[np.double_t, ndim=1] output,
                        np.ndarray[np.double_t, ndim=2] frame, int lx, int ly):

    cdef int i, k, l, ix, iy
    cdef float dx, dy, cx, cy, outsum

    for i in range(posx.shape[0]):
        if (posx[i] < 0) or (posx[i] > lx - 1) or (posy[i] < 0) or (posy[i] > ly - 1):
            output[i] = 0
        else:
            ix, iy = <int>posx[i] + 3, <int>posy[i] + 3
            dx, dy = posx[i] % 1, posy[i] % 1
            outsum = 0
            for k in range(6):
                cx, cy = fabs(dx - (k - 2)), fabs(dy - (k - 2))
                x[k] = M[0, k] + cx*M[1, k] + pow(cx, 2)*M[2, k] + pow(cx, 3)*M[3, k]
                y[k] = M[0, k] + cy*M[1, k] + pow(cy, 2)*M[2, k] + pow(cy, 3)*M[3, k]
            for k in range(6):
                for l in range(6):
                    outsum += frame[ix+k-2, iy+l-2]*x[k]*y[l]
            output[i] = outsum
    return output

