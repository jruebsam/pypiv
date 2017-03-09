Grid deformator class
=====================

The deformation of the grid for the window deformation is done by the GridDeformator class.

.. autoclass:: piv.grid_deformator.GridDeformator

After the initialization the velocities are set and a displacement is calculated.

.. automethod:: piv.grid_deformator.GridDeformator.set_velocities
.. automethod:: piv.grid_deformator.GridDeformator._get_displacement_function

In order to calculate the sub frame out of the displaced grid an other function must be invoked.

.. automethod:: piv.grid_deformator.GridDeformator.get_frame
