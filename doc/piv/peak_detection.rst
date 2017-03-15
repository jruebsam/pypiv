Peak detection algorithms
=========================

The function to call for the peak detection is a switch for the different methods.

.. autofunction:: piv.peak_detection.find_peak

It uses a function to check weather the maximum is inside or at the boarder of the correlation window.

.. autofunction:: piv.peak_detection.check_peak_position

The interpolation for the sub pixel shift has four different algorithms.

.. autofunction:: piv.peak_detection.gaussian
.. autofunction:: piv.peak_detection.centroid
.. autofunction:: piv.peak_detection.parabolic
.. autofunction:: piv.peak_detection.gaussian2D

.. ref on paper

