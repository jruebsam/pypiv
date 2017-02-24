.. pypiv documentation master file, created by
   sphinx-quickstart on Thu Feb 23 13:45:33 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pypiv's documentation!
=================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   directpiv
   velofilter


General Information
===================
This library calculates the particle image velocimetrie (piv) of a pair of images.
It consist of a Fourier based method to increase the performance.
In order to increase the accuracy, a window deformation Method is included as well.
The subpixel shift finder is implemented in two versions, each with it's downsides.
A detailed explanation of every module can be found by navigating through the contents.


Short description of PIV and its application
============================================
In particle image velocimetrie two images are compared in order to generate a vector field.
In these images interrogation windows are set an within these the mean displacement of the particles is calculated.
This is done by cross correlating the two interrogation windows, for which the fast fourier transform (FFT) is use.

To minimize the error, two methods are used:

* residual outlier detection
   this method uses a residual in a small neighbourhood around a point to determine weather that point is valid or not
* :doc:`Velocity Filter </velofilter>`
   this method calculates a maximum cutoff velocity and marks every velocity larger than this as not valid

After both of these methods the filtered values are interpolated.

After the first stage of the piv, an other can be set in order to reduce the error even further.
This is called an adaptiv piv.
With in these method the formerly chosen grid is deformed to capture particles in the flow with the previously calculated velocity.
These stages can be added up so that the grid can be refined or the error iteratively lowered.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
