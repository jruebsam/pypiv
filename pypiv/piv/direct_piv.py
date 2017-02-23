import numpy as np
from numpy.lib.stride_tricks import as_strided
from fft_correlator import FFTCorrelator
from grid_spec import GridSpec

class DirectPIV(object):
    """This class is the first Piv to be done.
    It creates a piv object, loads the images and sets the grid.
    """
    def __init__(self, image_a, image_b, window_size=32, search_size=32, distance=16):
        image_a, image_b = self._check_images(image_a, image_b)
        self.grid_spec = GridSpec(image_a.shape, image_a.strides,
                                   window_size, search_size, distance)

        self._correlator = FFTCorrelator(window_size, search_size)
        self._set_images(image_a, image_b)

        self.u = np.zeros(self.grid_spec.get_grid_shape())
        self.v = np.zeros_like(self.u)
        self._grid_creator()

    def _check_images(self, img_a, img_b):
        img_a, img_b = img_a.astype('float64'), img_b.astype('float64')
        if img_a.shape != img_b.shape:
            raise ValueError('Shape of the Images is not matching!')
        if img_a.strides != img_b.strides:
            raise ValueError('Stride of the Images is not matching!')
        return img_a, img_b

    def _set_images(self, img_a, img_b):
        '''Set the correlation images of the PIV algorithm'''
        self.frame_a = img_a
        pad = self.grid_spec.pad
        self._padded_fb = np.pad(img_b, 2*(pad,), 'constant')
        if self.grid_spec.pad == 0:
            self.frame_b = self._padded_fb
        else:
            self.frame_b = self._padded_fb[pad:-pad, pad:-pad]

    def _grid_creator(self):
        shape_fa    = self.grid_spec.get_interogation_grid_shape()
        shape_fb    = self.grid_spec.get_search_grid_shape()
        strides_fa  = self.grid_spec.get_interogation_grid_strides()
        strides_fb  = self.grid_spec.get_search_grid_strides()
        self.grid_a = as_strided(self.frame_a, strides=strides_fa, shape=shape_fa)
        self.grid_b = as_strided(self._padded_fb, strides=strides_fb, shape=shape_fb)

    def _get_window_frames(self, i, j):
        return self.grid_a[i, j], self.grid_b[i, j]

    def correlate_frames(self, method='gaussian'):
        for i, j in np.ndindex(self.grid_spec.get_grid_shape()):
            window_a, window_b = self._get_window_frames(i, j)
            displacement = (self._correlator.get_displacement(window_a, window_b,
                                                               subpixel_method=method))
            self.u[i, j] += displacement[0]
            self.v[i, j] += displacement[1]
        return  self.u, self.v

    def correlate_frames_2D(self):
        self.correlate_frames(method='9point')
