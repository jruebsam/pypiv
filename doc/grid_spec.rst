Class for grid specifications
=============================

In order to save the specifications of the grid a class in created.

.. autoclass:: piv.grid_spec.GridSpec

For comparing two GridSpec objects a operator is given.

.. automethod:: piv.grid_spec.GridSpec.equal_to

To get the information out of the class, getter functions are given.

.. automethod:: piv.grid_spec.GridSpec.get_grid_shape
.. automethod:: piv.grid_spec.GridSpec.get_interogation_grid_shape
.. automethod:: piv.grid_spec.GridSpec.get_search_grid_shape
.. automethod:: piv.grid_spec.GridSpec.get_interogation_grid_strides
.. automethod:: piv.grid_spec.GridSpec.get_search_grid_strides
