import numpy as np
from numpy.lib.stride_tricks import as_strided

from velocity_scaler import VelocityUpscaler
from grid_deformator import GridDeformator
from direct_piv import DirectPIV
from fft_correlator import FFTCorrelator
from grid_spec import GridSpec
from process import find_subpixel_peak

class AdaptivePIV(DirectPIV):
    def __init__(self, piv_object, window_size, search_size, distance):
        image_a, image_b = np.copy(piv_object.frame_a), np.copy(piv_object.frame_b)

        super(AdaptivePIV, self).__init__(image_a, image_b, window_size,
                                          search_size, distance)

        if self.grid_spec.equal_to(piv_object.grid_spec) == False:
            vs = VelocityUpscaler(self.grid_spec, piv_object.grid_spec)
            self.u = vs.scale_field(piv_object.u)
            self.v = vs.scale_field(piv_object.v)
        else:
            self.u, self.v = np.copy(piv_object.u), np.copy(piv_object.v)
        self._deform_grid()

    def _deform_grid(self):
        grid_def    = GridDeformator(self.frame_b, self.grid_spec)
        self.grid_b = grid_def.create_deformed_grid(self.u, self.v)

