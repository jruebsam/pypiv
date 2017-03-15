Filters for outlier detection
=============================

In order to remove outliers from the resulting vector field, filters are used.
The filter mainly used here differs from the :doc:`Velocity Filter <velofilter>`.

The filter initializes a mask of nan values in the velocity field.
It filters by calculating a local residual and comparing it with a threshold.

.. autofunction:: filters.outlier_from_local_median
.. autofunction:: filters.get_normalized_residual

The outliers are afterwards interpolated.

.. autofunction:: filters.replace_outliers
.. autofunction:: filters.replace_field

After the replacement of the outliers a median filter is applied to remove sharp edges.

.. autofunction:: filters.median_filter

