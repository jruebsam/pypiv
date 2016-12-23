import numpy as np

from velocity_scaler import VelocityUpscaler
from grid_deformator import GridDeformator
from direct_piv import DirectPIV
from grid_spec import GridSpec

class AdaptivePIV(DirectPIV):
    def __init__(self, piv_object, window_size, search_size, distance, ipmethod='bilinear'):
        image_a, image_b = np.copy(piv_object.frame_a), np.copy(piv_object.frame_b)

        super(AdaptivePIV, self).__init__(image_a, image_b, window_size,
                                          search_size, distance)

        if self.grid_spec.equal_to(piv_object.grid_spec):
            self.u, self.v = np.copy(piv_object.u), np.copy(piv_object.v)
        else:
            vscaler = VelocityUpscaler(self.grid_spec, piv_object.grid_spec)
            self.u = vscaler.scale_field(piv_object.u)
            self.v = vscaler.scale_field(piv_object.v)
        self._deform_grid(ipmethod)

    def _deform_grid(self, ipmethod):
        shape_b    = self.grid_spec.get_search_grid_shape()
        strides_b  = self.grid_spec.get_search_grid_strides()
        grid_def    = GridDeformator(self._padded_fb, shape_b, self.grid_spec.distance, ipmethod)
        self.grid_b = grid_def.create_deformed_grid(self.u, self.v)

