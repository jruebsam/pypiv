import numpy as np

from velocity_scaler import VelocityUpscaler
from grid_deformator import GridDeformator
from direct_piv import DirectPIV
from fft_correlator import FFTCorrelator

from process import find_subpixel_peak

class AdaptivePIV(object):
    def __init__(self, piv_object, window_size, search_size, distance):
        self._last_piv = piv_object
        self._interogation_ws = window_size
        self._search_ws = search_size
        self._distance = distance
        self._correlator = FFTCorrelator(window_size, search_size)
        #temporary solution
        self._newpiv = DirectPIV(np.copy(piv_object.frame_a),
                                 np.copy(piv_object.frame_b),
                                 window_size, search_size, distance)

        self._set_frames()

    def _set_frames(self):
        '''Set the correlation images of the PIV algorithm'''
        self._pad = max([0, (self._search_ws - self._interogation_ws)/2])
        self.frame_a = self._last_piv.frame_a
        self._padded_fb = np.pad(self._last_piv.frame_b, (self._pad, self._pad), 'constant')
        if self._pad == 0:
            self.frame_b = self._padded_fb
        else:
            self.frame_b = self._padded_fb[self._pad:-self._pad, self._pad:-self._pad]

    def _scale_velocities(self):
        last_inter  = self._last_piv._interogation_ws
        last_search = self._last_piv._search_ws
        last_dist   = self._last_piv._distance

        new_inter  = self._interogation_ws
        new_search = self._search_ws
        new_dist = self._distance

        cond1 = new_inter == last_inter
        cond2 = new_search == last_search
        cond3 = new_dist == last_dist

        if cond1 & cond2 & cond3:
            self.u = self._last_piv.u
            self.v = self._last_piv.v
        else:
            vs = VelocityUpscaler(self._last_piv.frame_b,
                                  last_inter, last_dist,
                                   new_inter,  new_dist)

            self.u = vs.scale_field(self._last_piv.u)
            self.v = vs.scale_field(self._last_piv.v)

    def correlate_frames(self):
        self._scale_velocities()
        g = GridDeformator(self.frame_b, self._interogation_ws ,
                           self._search_ws, self._distance )

        grid_a = self._newpiv.grid_a
        grid_b = g.create_deformed_grid(self.u, self.v)

        for i, j in np.ndindex(grid_a.shape[:2]):
            displacement = (self._correlator
                            .get_displacement(grid_a[i, j], grid_b[i, j]))
            self.u[i, j] += displacement[0]
            self.v[i, j] += displacement[1]

        return  self.u, self.v

    def correlate_frames_2D(self):
        self._scale_velocities()
        g = GridDeformator(self.frame_b, self._interogation_ws ,
                           self._search_ws, self._distance )

        grid_a = self._newpiv.grid_a
        grid_b = g.create_deformed_grid(self.u, self.v)

        for i, j in np.ndindex(grid_a.shape[:2]):
            displacement = (self._correlator
                            .get_displacement(grid_a[i, j], grid_b[i, j],subpixel_method='9point'))
            self.u[i, j] += displacement[0]
            self.v[i, j] += displacement[1]

        return  self.u, self.v
