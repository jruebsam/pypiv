.. pypiv documentation master file, created by
   sphinx-quickstart on Thu Feb 23 13:45:33 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pypiv's documentation!
=================================
The pypiv API is developed by the pypiv Developmentteam in 2016 and 2017 under the BSD3 clause.
Initially designed to perform particle image velocimetry for double diffusive convection, the API is also capable of many more tasks.
The Usage, described below is optimized for fluid flow and the API is not yet tested for more applications.


General Information
===================
This library calculates the particle image velocimetry (piv) of a pair of images.
It consist of a Fourier based method to increase the performance.
In order to increase the accuracy, a window deformation Method is included as well.
The sub pixel shift finder is implemented in two versions, each with it's downsides.
A detailed explanation of every module can be found by navigating through the contents.


Short description of PIV and its application
============================================
In particle image velocimetry two images are compared in order to generate a vector field.
In these images interrogation windows are set an within these the mean displacement of the particles is calculated.
This is done by cross correlating the two interrogation windows, for which the fast Fourier transform (FFT) is use.

To minimize the error, two methods are used:

* :doc:`residual outlier detection <piv/filters>`
   this method uses a residual in a small neighbourhood around a point to determine weather that point is valid or not
* :doc:`Velocity Filter <piv/velofilter>`
   this method calculates a maximum cutoff velocity and marks every velocity larger than this as not valid

After both of these methods the filtered values are interpolated.

After the first stage of the piv, an other can be set in order to reduce the error even further.
This is called an adaptive piv.
With in these method the formerly chosen grid is deformed to capture particles in the flow with the previously calculated velocity.
These stages can be added up so that the grid can be refined or the error iteratively lowered.

Examples
========
In order to test the library quickly and show its potential an example folder is added.
It contains test images of a double diffusive convection flow which are of analytically nature.
These show results of a single direct piv and multiple adaptive piv.

Early on the library had issues with 180 degree rotation.
To show this issue, a mirror test has been added.
It computes two times the same setup.
One with the original image and a second with the image mirrored.
This issue is still unsolved.

An other test is added for the sub pixel peak detection.
The accuracy of a piv process is still relying on weak peak fitting algorithms.
These perform two times a one dimensional fit on the correlation peak.
The reason for these is that they are much faster, then the competition.
Problematic is that the show the pixel locking effect, which means the have a very small error for very small sub pixel shifts.
This calculated by the example "test_subpeak_methods".
With this the maximum error is calculated for various sizes of the correlation peak.
In order to compensate this error a real two dimensional gaussian interpolation method is added.
It can reduce the maximum error by some orders of magnitude.

.. image:: _static/max_error_subpeak_windowsize_32.png

The image shows the result of that example after 1000 randomly chosen shifts for each diameter for the different methods.
The error axis is plotted logarithmically.
The correlation window size is in this case comparable to the interrogation window size used for the piv (32x32).
As one can see that the two times one dimensional methods have a almost constant maximum error of about 0.5 pixel.
The newly implemented method for the real two dimensional gaussian interpolation has a minimum some orders of magnitude below the other methods but it is also much worse for diameters smaller and about a pixel.
But this comes with the price of a longer calculation time, which can also be observed with that example.

.. image:: _static/mean_error_subpeak_windowsize_32.png

The two times one dimensional interpolation methods do show a large maximum error.
But considering the mean error of 1000 trials as shown in the image above the error is tolerable.
The error bars are calculated by the standard deviation of the trials.
This can also be calculated by the example mentioned above.

Test
====
In order to assure the usability of the API unittest have been added.
These test every component of the API separately.
For these the pytest API has to be installed.
The test are located in the test folder of the root directory.


API Documentation
=================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   ./piv/direct_piv
   ./piv/grid_spec
   ./piv/fft_correlator
   ./piv/peak_detection
   ./piv/adaptiv_piv
   ./piv/velocity_scaler
   ./piv/interpolator
   ./piv/grid_deformator
   ./piv/velofilter
   ./piv/filters


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
