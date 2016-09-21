from velocity_scaler import VelocityUpscaler
from grid_deformator import GridDeformator

class AdaptivePIV(object):
    def __init__(self, piv_object, window_size, search_size, distance):
        self._last_piv = piv_object
        self._interogation_ws = window_size
        self._search_ws = search_size
        self._distance = distance

    def _scale_velocities(self):
        last_inter  = self._last_piv._interogation_ws
        last_search = self._last_piv._search_ws
        new_inter  = self._interogation_ws
        new_search = self._search_ws

        v = VelocityUpscaler(self._last_piv.frame_b,
                             last_inter, last_search,
                              new_inter,  new_search)

        self.u = v.scale_field(self._last_piv.u)
        self.v = v.scale_field(self._last_piv.v)

    def correlate_frames():
        self._scale_velocities()
        g = geopiv.GridDeformator(self._last_piv.frame_b,
                                  self._interogation_ws,
                                  self._search_ws, self._distance )

        grid_a = self._last_piv.grid_a
        grid_b = g.create_deformed_grid(self.u, self.v)

        lx, ly, _, _ = self.grid_a.shape
        self.u = np.empty((lx, ly))
        self.v = np.empty((lx, ly))
        for i in range(lx):
            for j in range(ly):
                correlation = self._correlator.evaluate_windows(self.grid_a[i, j],
                                                                self.grid_b[i, j])

                xi, yi = find_subpixel_peak(correlation, subpixel_method='gaussian')
                cx, cy = correlation.shape
                corr_pad = (self._search_ws - self._interogation_ws)/2.
                self.u[i, j] = (cx/2. - xi - corr_pad)/self.dt
                self.v[i, j] = (cy/2. - yi - corr_pad)/self.dt
        return  self.u, self.v
