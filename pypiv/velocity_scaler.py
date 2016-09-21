import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import RectBivariateSpline as RBS

class VelocityUpscaler(object):
    def __init__(self, frame, window_size=32, distance=16,\
            target_window_size=32, target_distance=10):
        self._frame = frame
        self._ws = window_size
        self._dist = distance
        self._tw = target_window_size
        self._td = target_distance

        lx, ly  = self._get_field_shape(frame, window_size, distance)
        self._tx  = np.arange(0, lx*distance, distance)
        self._ty  = np.arange(0, ly*distance, distance)

        lx, ly  = self._get_field_shape(frame,target_window_size, target_distance)
        self._lx, self._ly = lx, ly
        tx  = np.arange(0, lx*target_distance, target_distance)
        ty  = np.arange(0, ly*target_distance, target_distance)
        self._out_x, self._out_y = np.meshgrid(tx, ty, indexing='ij')

    def _get_field_shape(self, frame, window_size, distance):
        lx, ly = frame.shape
        return ((lx - window_size)//distance+1, (ly - window_size)//distance+1)

    def scale_field(self, f):
        rbs = RBS(self._tx, self._ty, f)
        return rbs.ev(self._out_x, self._out_y)
