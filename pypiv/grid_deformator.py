import numpy as np
from numpy.lib.stride_tricks import as_strided
from scipy.interpolate import RectBivariateSpline as RBS
from scipy.ndimage import map_coordinates

class GridDeformator(object):
    def __init__(self, frame_b, window_size=32, search_size=32, distance=16):
        self._interogation_ws = window_size
        self._search_ws= search_size
        self._distance = distance
        self._set_frames(frame_b)
        self._frame_grid_creator()
        self._pos_grid_creator()

    def _set_frames(self, frame_b):
        self._pad = max([0, (self._search_ws - self._interogation_ws)/2])
        self._padded_fb = np.pad(frame_b, (self._pad, self._pad), 'constant')
        if self._pad == 0:
            self.frame_b = self._padded_fb
        else:
            self.frame_b = self._padded_fb[self._pad:-self._pad, self._pad:-self._pad]

    def _frame_grid_creator(self):
        distance = self._distance
        shape = self._get_field_shape(self.frame_b, self._interogation_ws, distance)
        self._shape_b = shape + 2*(self._search_ws,)
        sx, sy = self._padded_fb.strides
        strides_b = (sx*distance, sy*distance, sx, sy)
        self._bgrid = as_strided(self._padded_fb, strides=strides_b, shape=self._shape_b)

    def _pos_grid_creator(self):
        distance = self._distance
        lx, ly = self._padded_fb.shape
        self._pos_x, self._pos_y = np.mgrid[0:lx, 0:ly]
        sx, sy = self._pos_x.strides
        strides_pos = (sx*distance, sy*distance, sx, sy)
        self._grid_x = as_strided(self._pos_x, strides=strides_pos, shape=self._shape_b)
        self._grid_y = as_strided(self._pos_y, strides=strides_pos, shape=self._shape_b)

    def _get_field_shape(self, frame, window_size, distance):
        lx, ly = frame.shape
        return ((lx - window_size)//distance+1, (ly - window_size)//distance+1)

    def _set_displacements_fields(self, u, v):
        self._u_disp = self._get_displacement_function(u)
        self._v_disp = self._get_displacement_function(v)

    def _get_displacement_function(self, f):
        dx = self._distance
        f_x,  f_y  = np.gradient(f  , dx)
        f_xx, f_xy = np.gradient(f_x, dx)
        f_yx, f_yy = np.gradient(f_y, dx)
        return lambda i, j, x, y : f[i, j] + x*f_x[i, j]  + y*f_y[i, j]\
                    + 0.5*(f_xx[i, j]*x**2 + 2*f_xy[i, j]*x*y + f_yy[i, j]*y**2)

    def create_deformed_grid(self, u, v):
        #warum ????
        self._set_displacements_fields(u, v)
        gx = self._grid_x
        gy = self._grid_y
        lx, ly, _, _ =  gx.shape

        dws = self._search_ws/2.
        offset_x, offset_y = np.mgrid[-dws:dws, -dws:dws]

        '''
        plt.imshow(u, extent=[0, 1024, 0, 1024])
        ptsax =[]
        ptsay =[]
        for i in range(lx):
            for j in range(ly):
                if (i%4 ==0 ) and (j%4==0):
                    ptsax.append(gx[i, j])
                    ptsay.append(gy[i, j])
        ptsax = np.array(ptsax)
        ptsay = np.array(ptsay)
        plt.scatter(ptsax, ptsay , c ='red', lw=0.5, alpha=0.5, edgecolor='none')
        p1, p2 = [], []
        '''
        ptsax = np.zeros(gx.shape)
        ptsay = np.zeros(gx.shape)

        for i in range(lx):
            for j in range(ly):
                ptsax[i, j] = gx[i, j] + self._u_disp(i, j, offset_x, offset_y)
                ptsay[i, j] = gy[i, j] + self._v_disp(i, j, offset_x, offset_y)
        '''
                if (i%4 ==0 ) and (j%4==0):
                    p1.append(ptsax[i, j])
                    p2.append(ptsay[i, j])
        p1 = np.array(p1).flatten()
        p2 = np.array(p2).flatten()
        plt.scatter(p1, p2, c ='green', lw=0.5, alpha=0.5, edgecolor='none')
        plt.show()
        '''
        #xn, yn =  self._padded_fb.shape
        #rbs = RBS(np.arange(xn), np.arange(yn),  self._padded_fb)

        out = np.zeros(v.shape+2*(self._search_ws,))
        for i in range(lx):
            for j in range(ly):
                #out[i, j]  =  rbs.ev(ptsax[i, j], ptsay[i, j])
                p, q = ptsax[i, j].shape
                test =   ndimage.map_coordinates(self._padded_fb, [ptsax[i, j].flatten(), ptsay[i, j].flatten()], order=1).reshape(p, q)
                out[i,j] = test

        return out

    def test(self):
        gx = self._grid_x
        gy = self._grid_y
        lx, ly, _, _ =  gx.shape

        for i in range(lx):
            for j in range(ly):
                gx[i, j] += 1
                gy[i, j] += 1

        f, (ax1, ax2) = plt.subplots(1, 2)
        ax1.imshow(self._pos_x)
        ax2.imshow(self._pos_y)
        plt.show()


