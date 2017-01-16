import numpy as np

from velocity_scaler import VelocityUpscaler
from grid_deformator import GridDeformator
from direct_piv import DirectPIV
from grid_spec import GridSpec

class AdaptivePIV(DirectPIV):
    def __init__(self, piv_object, window_size, search_size, distance, deformation='forward', ipmethod='bilinear'):
        image_a, image_b = np.copy(piv_object.frame_a), np.copy(piv_object.frame_b)

        super(AdaptivePIV, self).__init__(image_a, image_b, window_size,
                                          search_size, distance)

        if self.grid_spec.equal_to(piv_object.grid_spec):
            self.u, self.v = np.copy(piv_object.u), np.copy(piv_object.v)
        else:
            vscaler = VelocityUpscaler(self.grid_spec, piv_object.grid_spec)
            self.u = vscaler.scale_field(piv_object.u)
            self.v = vscaler.scale_field(piv_object.v)
        self._deformation_method = deformation
        self._deform_grid(deformation, ipmethod)

    def _deform_grid(self, deformation_method, ipmethod):
        distance   = self.grid_spec.distance
        shape_b    = self.grid_spec.get_search_grid_shape()
        if deformation_method == 'central':
            shape_a    = self.grid_spec.get_interogation_grid_shape()

            self.grid_def_a  = GridDeformator(self.frame_a, shape_a, distance, ipmethod)
            self.grid_def_a.set_velocities(-self.u/2, -self.v/2.)

            self.grid_def_b  = GridDeformator(self._padded_fb, shape_b, distance, ipmethod)
            self.grid_def_b.set_velocities(self.u/2., self.v/2.)

        if deformation_method == 'forward':
            self.grid_def_b  = GridDeformator(self._padded_fb, shape_b, distance, ipmethod)
            self.grid_def_b.set_velocities(self.u, self.v)

    def _get_window_frames(self, i, j):
        if self._deformation_method == 'central':
            frame_a = self.grid_def_a.get_frame(i, j)
            frame_b = self.grid_def_b.get_frame(i, j)
        if self._deformation_method == 'forward':
            frame_a = self.grid_a[i, j]
            frame_b = self.grid_def_b.get_frame(i, j)
        return frame_a, frame_b




