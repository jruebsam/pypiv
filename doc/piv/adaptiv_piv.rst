Class for adaptiv Piv
=====================

The sub class for the iterative part of the piv process is called Adaptive Piv.

.. autoclass:: piv.adaptive_piv.AdaptivePIV

In order to perform the deformation and needed interpolation a new method is introduced.

.. automethod:: piv.adaptive_piv.AdaptivePIV._deform_grid

For inclusion of these two different deformation methods into the correlation, the function getting the sub images has to be overridden.

.. automethod:: piv.adaptive_piv.AdaptivePIV._get_window_frames

