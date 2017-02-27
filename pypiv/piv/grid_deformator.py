import numpy as np
from numpy.lib.stride_tricks import as_strided
from scipy.ndimage import map_coordinates
import sys
from interpolator import CubicInterpolator

class GridDeformator(object):
    """
    Class of the grid deformator.
    """

    def __init__(self, frame, shape, distance, method='bilinear'):
        """
        Initialization of the grid deformation process.

        The frame and grid shape are set as well as the distance between the interrogation windows and the method of deformation.
        The avaliable methods are

        * bilinear and 
        * central.

        :param frame: image that is interpolated
        :param shape: shape of the initial regular grid
        :param distance: shift between the interogation windows
        :param method: deformation method
        """
        self._frame  = frame
        self._shape  = shape
        self._distance = distance
        self._ipmethod = method
        if method == 'cubic':
            self._cube_ip = CubicInterpolator(frame, shape[-1])

    def set_velocities(self, u, v):
        """
        Setter function for the veloceties to calculate the displacement.

        Calls the getter function for every velocity component.

        :param u: x komponent of the velocity vector
        :param v: y komponent of the velocity vector
        """
        self._u_disp = self._get_displacement_function(u)
        self._v_disp = self._get_displacement_function(v)

    def _get_displacement_function(self, f):
        """
        Getter function for calculating the displacement.

        :param f: field that is used for the displacement, mainly velocity komponents
        :returns: function of the taylored field to first order
        """
        dx = self._distance
        f_x,  f_y  = np.gradient(f  , dx)
        f_xx, f_xy = np.gradient(f_x, dx)
        f_yx, f_yy = np.gradient(f_y, dx)
        return lambda i, j, x, y : (f[i, j] + x*f_x[i, j]  + y*f_y[i, j]
                       + 0.5*(f_xx[i, j]*x**2 + 2*f_xy[i, j]*x*y + f_yy[i, j]*y**2))

        #For the bilinear method the build in scipy method `map_coordinates <https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.interpolation.map_coordinates.html>`_ is used with *order* set to 1.
    def get_frame(self, i, j):
        """
        Perform interpolation to produce the deformed window for correlation.

        This function takes the previosly set displacement and interpolates the image for these corrdinates.
        If the cubic interpolation method is choosen, the cubic interpolation of this API is use.
        For the bilinear method the build in scipy method `map_coordinates <https://goo.gl/wucmUO>`_ is used with *order* set to 1.

        :param int i: first index in grid coordinates
        :param int j: second index in grid coordinates
        :returns: interpolated window for the grid coordinates i,j and the image set in initialization
        """
        dws = self._shape[-1]
        offset_x, offset_y = np.mgrid[-dws/2+0.5:dws/2+0.5, -dws/2+0.5:dws/2+0.5]

        gx, gy = np.mgrid[0:dws, 0:dws]

        grid_x = gx + self._distance*i
        grid_y = gy + self._distance*j

        ptsax = (grid_x + self._u_disp(i, j, offset_x, offset_y)).ravel()
        ptsay = (grid_y + self._v_disp(i, j, offset_x, offset_y)).ravel()
        p, q = self._shape[-2:]

        if self._ipmethod == 'bilinear':
            return map_coordinates(self._frame, [ptsax, ptsay], order=1).reshape(p, q)
        if self._ipmethod == 'cubic':
            return  self._cube_ip.interpolate(ptsax, ptsay).reshape(p, q)

