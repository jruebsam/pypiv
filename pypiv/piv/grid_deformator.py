import numpy as np
from numpy.lib.stride_tricks import as_strided
from scipy.ndimage import map_coordinates
import sys
from interpolator import CubicInterpolator

class GridDeformator(object):
    def __init__(self, frame, shape, distance, method='bilinear'):
        self._frame  = frame
        self._shape  = shape
        self._distance = distance
        self._ipmethod = method
        if method == 'cubic':
            self._cube_ip = CubicInterpolator(frame, shape[-1])

    def set_velocities(self, u, v):
        self._u_disp = self._get_displacement_function(u)
        self._v_disp = self._get_displacement_function(v)

    def _get_displacement_function(self, f):
        dx = self._distance
        f_x,  f_y  = np.gradient(f  , dx)
        f_xx, f_xy = np.gradient(f_x, dx)
        f_yx, f_yy = np.gradient(f_y, dx)
        return lambda i, j, x, y : (f[i, j] + x*f_x[i, j]  + y*f_y[i, j]
                       + 0.5*(f_xx[i, j]*x**2 + 2*f_xy[i, j]*x*y + f_yy[i, j]*y**2))

    def get_frame(self, i, j):
        dws = self._shape[-1]
        offset_x, offset_y = np.mgrid[-dws/2+0.5:dws/2+0.5, -dws/2+0.5:dws/2+0.5]

        gx, gy = np.mgrid[0:dws, 0:dws]

        grid_x = gx + self._distance*i
        grid_y = gy + self._distance*j

        ptsax = (grid_x + self._u_disp(i, j, offset_x, offset_y)).ravel()
        ptsay = (grid_y + self._v_disp(i, j, offset_x, offset_y)).ravel()
        p, q = self._shape[-2:]

        if self._ipmethod == 'bilinear':
            return map_coordinates(self._frame, [ptsax, ptsay], order=1).reshape(p, q)
        if self._ipmethod == 'cubic':
            return  self._cube_ip.interpolate(ptsax, ptsay).reshape(p, q)

