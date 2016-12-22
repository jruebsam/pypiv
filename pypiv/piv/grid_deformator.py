import numpy as np
from numpy.lib.stride_tricks import as_strided
from scipy.ndimage import map_coordinates
import sys

class GridDeformator(object):
    def __init__(self, frame, shape, distance):
        self._frame  = frame
        self._shape  = shape
        self._window_size = shape[-1]
        self._distance = distance
        self._pos_grid_creator()

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

        out = np.zeros(v.shape+2*(self._window_size,))
        for i, j in np.ndindex(self._shape[:2]):
            p, q = ptsax[i, j].shape
            '''
            sample = map_coordinates(self._frame,
                    [ptsax[i, j].flatten(), ptsay[i, j].flatten()], order=1).reshape(p, q)
            out[i,j] = sample
            '''
            print i, j
            for  k in range(p):
                for l in range(q):
                    out[i, j, k, l] = self._test_cubic(ptsax[i, j, k, l], ptsay[i, j, k, l])
            #if j>30:
            #    sys.exit(1)
        return out

    def _test_cubic(self, x, y):
        pos_x, dx = divmod(x, 1)
        pos_y, dy = divmod(y, 1)

        pos = np.array([-2.5, -1.5, -0.5, 0.5, 1.5, 2.5])
        x = np.abs(dx - pos)
        y = np.abs(dy - pos)

        M  = np.array([[-18./5.,  14./5.,     1.,     1.,  14./5., -18/5.],
                       [ 21./5., -27./5.,     0.,     0., -27./5., 21./5.],
                       [ -8./5.,  16./5., 11./5., 11./5.,  16./5., -8./5.],
                       [  1./5.,  -3./5.,  6./5.,  6./5.,  -3./5.,  1./5.]])

        outx = M[0] + x*M[1] + x**2*M[2] + x**3*M[3]
        outy = M[0] + y*M[1] + y**2*M[2] + y**3*M[3]
        out  = np.outer(outx, outy)

        frame_window = self._frame[pos_x-2:pos_x+4, pos_y-2:pos_y+4]

        try:
            out = np.sum(out*frame_window)
        except:
            out = 0
        return out
