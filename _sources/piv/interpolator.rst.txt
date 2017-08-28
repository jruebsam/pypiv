Cubic interpolator
==================

The cubic interpolator is written as its own class.

.. autoclass:: piv.interpolator.CubicInterpolator

It performs the interpolation by calling the interpolate function.

.. automethod:: piv.interpolator.CubicInterpolator.interpolate

The interpolation function itself is not a method of that class, but a part of the interpolator module.
The entire module is compiled with Cython in order to decrease the computation time.

