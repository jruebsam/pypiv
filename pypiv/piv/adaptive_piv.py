import numpy as np
from numpy.lib.stride_tricks import as_strided

from velocity_scaler import VelocityUpscaler
from grid_deformator import GridDeformator
from direct_piv import DirectPIV
from fft_correlator import FFTCorrelator
from grid_spec import GridSpec
from process import find_subpixel_peak

class AdaptivePIV(object):
    def __init__(self, piv_object, window_size, search_size, distance):

        image_a, image_b = np.copy(piv_object.frame_a), np.copy(piv_object.frame_b)
        self.grid_spec = GridSpec(image_a.shape, image_a.strides,
                                   window_size, search_size, distance)

        if self.grid_spec.equal_to(piv_object.grid_spec) == False:
            vs = VelocityUpscaler(self.grid_spec, piv_object.grid_spec)
            self.u = vs.scale_field(piv_object.u)
            self.v = vs.scale_field(piv_object.v)
        else:
            self.u, self.v = np.copy(piv_object.u), np.copy(piv_object.v)

        self._correlator = FFTCorrelator(window_size, search_size)
        self._set_images(image_a, image_b)
        self._grid_creator()

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
        strides_fa  = self.grid_spec.get_interogation_grid_strides()
        self.grid_a = as_strided(self.frame_a, strides=strides_fa, shape=shape_fa)

        grid_def    = GridDeformator(self.frame_b, self.grid_spec)
        self.grid_b = grid_def.create_deformed_grid(self.u, self.v)

    def correlate_frames(self, method='gaussian'):
        lx, ly, _, _ = self.grid_a.shape
        for i, j in np.ndindex(self.grid_a.shape[:2]):
            displacement = (self._correlator .get_displacement(self.grid_a[i, j],
                                                               self.grid_b[i, j],
                                                               subpixel_method=method))
            self.u[i, j] += displacement[0]
            self.v[i, j] += displacement[1]
        return  self.u, self.v

    def correlate_frames_2D(self):
        self.correlate_frames(method='9point')
