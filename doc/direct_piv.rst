Class for direct Piv
====================

The base class for the piv process is called Direct Piv.

.. autoclass:: piv.direct_piv.DirectPIV

In order to make sure that the images used have to correct type and layout and are set, the functions

.. automethod:: piv.direct_piv.DirectPIV._check_images

.. automethod:: piv.direct_piv.DirectPIV._set_images

are used.

The initialization requires a grid to be set.
Therefore a function creates the grid according to the GridSpec.

.. set ref ones included
.. automethod:: piv.direct_piv.DirectPIV._grid_creator

After all the initialization is done the correlation can be performed by calling the correlation function.

.. automethod:: piv.direct_piv.DirectPIV.correlate_frames

The parameter of this function controls the algorithm of the peak finder.
Read more about this in the documentation of the process module.

.. set ref to module process ones included

If an explicitly two dimensional peak finder is needed, a function which handles this is also included.

.. automethod:: piv.direct_piv.DirectPIV.correlate_frames_2D

These methods call an other method in order to extract the sub image needed for a step.

.. automethod:: piv.direct_piv.DirectPIV._get_window_frames

