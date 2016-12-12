import numpy as np
from numpy.lib.stride_tricks import as_strided
from fft_correlator import FFTCorrelator

class DirectPIV(object):
    def __init__(self, image_a, image_b, window_size=32, search_size=32, distance=16):
        self._interogation_ws = window_size
        self._search_ws= search_size
        self._distance = distance
        self._correlator = FFTCorrelator(window_size, search_size)

        self._set_images(image_a, image_b)
        self._grid_creator()


    def _set_images(self, img_a, img_b):
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

        self.grid_a = as_strided(self.frame_a, strides=strides_a, shape=shape_a)
        self.grid_b = as_strided(self._padded_fb, strides=strides_b, shape=shape_b)

    def _get_field_shape(self):
        lx, ly = self.frame_a.shape
        return ((lx - self._interogation_ws)//self._distance+1,
                (ly - self._interogation_ws)//self._distance+1)

    def correlate_frames(self):
        lx, ly, _, _ = self.grid_a.shape
        self.u, self.v = np.empty((lx, ly)), np.empty((lx, ly))
        for i, j in np.ndindex(self.grid_a.shape[:2]):
            self.u[i,j], self.v[i, j] = (self._correlator .get_displacement(
                                         self.grid_a[i, j], self.grid_b[i, j]))

        return  self.u, self.v

    def correlate_frames_2D(self):
        lx, ly, _, _ = self.grid_a.shape
        self.u, self.v = np.empty((lx, ly)), np.empty((lx, ly))
        for i, j in np.ndindex(self.grid_a.shape[:2]):
            self.u[i,j], self.v[i, j] = (self._correlator .get_displacement_2D(
                                         self.grid_a[i, j], self.grid_b[i, j],
											subpixel_method='9point'))

        return  self.u, self.v

