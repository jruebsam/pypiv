import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import RectBivariateSpline as RBS


class VelocityUpscaler(object):
    """
    Class for scaling the velocity field according to GridSpec
    """

    def __init__(self, new_grid_spec, old_grid_spec):
        """
        Initialization of the scaler.

        The old and new grid specifications are loaded and a meshgrid according to the new grid is calculated.

        :param GridSpec new_grid_spec: GridSpec of the new field
        :param GridSpec old_grid_spec: GridSpec of the old field
        """
        self.new_spec = new_grid_spec
        self.old_spec = old_grid_spec

        self._ws = old_grid_spec.window_size
        self._dist = old_grid_spec.distance

        self._tw = new_grid_spec.window_size
        self._td = new_grid_spec.distance

        lx, ly = old_grid_spec.get_grid_shape()
        distance = old_grid_spec.distance

        self._tx  = np.arange(0, lx*distance, distance)
        self._ty  = np.arange(0, ly*distance, distance)

        lx, ly = new_grid_spec.get_grid_shape()
        target_distance = new_grid_spec.distance

        tx  = np.arange(0, lx*target_distance, target_distance)
        ty  = np.arange(0, ly*target_distance, target_distance)
        self._out_x, self._out_y = np.meshgrid(tx, ty, indexing='ij')

    def scale_field(self, f):
        """
        Scaling of the field according to calculated meshgrid.

        For the interpolation rectangualr bivariant Splines are used.
        These are implemented from the scipy function `RectBivariateSpline <https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.RectBivariateSpline.html>`_.

        :param f: field to be interpolated
        :returns: field after interpolation
        """
        rbs = RBS(self._tx, self._ty, f)
        return rbs.ev(self._out_x, self._out_y)
