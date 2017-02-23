Documentation of the Velocity Filter
====================================

In order to reduce the amount of outliers in the piv result a velocity filter is implemented.
This filter is called from the main function:

.. autofunction:: velofilter.filter

In order to calculate the results a calculation of the velocities in an histogram like for and the integral over that is needed.
The binning is done by the function

.. autofunction:: velofilter.calc_derivative

The integral over that is calculated as well directly from the data by the function

.. autofunction:: velofilter.calc_factor
