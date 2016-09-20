import numpy as np
from numpy.lib.stride_tricks import as_strided
from fft_correlator import FFTCorrelator
from process import find_subpixel_peak

class DirectPIV(object):
    def __init__(self, window_size=32, search_size=32, distance=16, dt=1.):
        self._interogation_ws = window_size
        self._search_ws= search_size
        self._distance = distance
        self._dt = dt
        self._correlator = FFTCorrelator(window_size, search_size)

    def set_images(self, img_a, img_b):
        '''Set the correlation images of the PIV algorithm'''
        img_a = img_a.astype('float64')
        img_b = img_b.astype('float64')

        self._pad = max([0, (self._search_ws - self._interogation_ws)/2])
        self.frame_a = img_a
        self._padded_fb = np.pad(img_b, (self._pad, self._pad), 'constant')
        if self._pad == 0:
            self.frame_b = self._padded_fb
        else:
            self.frame_b = self._padded_fb[self._pad:-self._pad, self._pad:-self._pad]

    def _grid_creator(self):
        distance = self._distance
        shape = self._get_field_shape()

        shape_a = shape + 2*(self._interogation_ws,)
        shape_b = shape + 2*(self._search_ws,)

        sx, sy = self.frame_a.strides
        strides_a = (sx*distance, sy*distance, sx, sy)

        sx, sy = self._padded_fb.strides
        strides_b = (sx*distance, sy*distance, sx, sy)

        self._grid_a = as_strided(self.frame_a, strides=strides_a, shape=shape_a)
        self._grid_b = as_strided(self._padded_fb, strides=strides_b, shape=shape_b)

    def _get_field_shape(self):
        lx, ly = self.frame_a.shape
        return ((lx - self._interogation_ws)//self._distance+1,
                (ly - self._interogation_ws)//self._distance+1)

    def correlate_frames(self):
        self._grid_creator()
        lx, ly, _, _ = self._grid_a.shape
        self.u = np.empty((lx, ly))
        self.v = np.empty((lx, ly))
        for i in range(lx):
            for j in range(ly):
                correlation = self._correlator.evaluate_windows(self._grid_a[i, j],
                                                                self._grid_b[i, j])

                xi, yi = find_subpixel_peak(correlation, subpixel_method='gaussian')
                cx, cy = correlation.shape
                corr_pad = (self._search_ws - self._interogation_ws)/2.
                self.u[i, j] = (cx/2. - xi - corr_pad)/self._dt
                self.v[i, j] = (cy/2. - yi - corr_pad)/self._dt
        return  self.u, self.v

