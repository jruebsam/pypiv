import numpy as np
from numpy.lib.stride_tricks import as_strided
from scipy.ndimage import map_coordinates
import sys
from interpolator import cubic_interpolation

class GridDeformator(object):
    def __init__(self, frame, shape, distance, method='bilinear'):
        self._frame  = frame
        self._shape  = shape
        self._window_size = shape[-1]
        self._distance = distance
        self._pos_grid_creator()
        self._ipmethod = method

    def _pos_grid_creator(self):
        lx, ly = self._frame.shape
        self._pos_x, self._pos_y = np.mgrid[0:lx, 0:ly]
        sx, sy = self._pos_x.strides
        strides_pos = (sx*self._distance, sy*self._distance, sx, sy)
        self.grid_x = as_strided(self._pos_x, strides=strides_pos, shape=self._shape)
        self.grid_y = as_strided(self._pos_y, strides=strides_pos, shape=self._shape)

    def _set_displacements_fields(self, u, v):
        self._u_disp = self._get_displacement_function(u)
        self._v_disp = self._get_displacement_function(v)

    def _get_displacement_function(self, f):
        dx = self._distance
        f_x,  f_y  = np.gradient(f  , dx)
        f_xx, f_xy = np.gradient(f_x, dx)
        f_yx, f_yy = np.gradient(f_y, dx)
        return lambda i, j, x, y : (f[i, j] + x*f_x[i, j]  + y*f_y[i, j]
                       + 0.5*(f_xx[i, j]*x**2 + 2*f_xy[i, j]*x*y + f_yy[i, j]*y**2))

    def create_deformed_grid(self, u, v):
        self._set_displacements_fields(u, v)
        dws = self._window_size/2.
        offset_x, offset_y = np.mgrid[-dws+0.5:dws+0.5, -dws+0.5:dws+0.5]
        ptsax = np.zeros(self.grid_x.shape)
        ptsay = np.zeros_like(ptsax)

        for i, j in np.ndindex(self._shape[:2]):
            ptsax[i, j] = self.grid_x[i, j] + self._u_disp(i, j, offset_x, offset_y)
            ptsay[i, j] = self.grid_y[i, j] + self._v_disp(i, j, offset_x, offset_y)

        out = np.zeros(self._shape)
        if self._ipmethod == 'bilinear':
            for i, j in np.ndindex(self._shape[:2]):
                    p, q = ptsax[i, j].shape
                    sample = map_coordinates(self._frame,
                            [ptsax[i, j].flatten(), ptsay[i, j].flatten()], order=1).reshape(p, q)
                    out[i,j] = sample
        if self._ipmethod == 'cubic':
            padded_frame = np.pad(self._frame, (3, 3), mode='constant')
            out = cubic_interpolation(ptsax.flatten(), ptsay.flatten(),\
                                      padded_frame, len(self._frame)).reshape(self._shape)
        return out

