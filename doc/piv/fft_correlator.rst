Class for the FFT correlator
============================

For calculating the correlation with fast Fourier Transform (FFT) a class is set up.

.. autoclass:: piv.fft_correlator.FFTCorrelator

If the window size does not meet the needs of the FFT function, the windows get padded with zeros.

.. automethod:: piv.fft_correlator.FFTCorrelator._set_padding

By calling the function for the getting the displacement the correlation is performed as well

.. automethod:: piv.fft_correlator.FFTCorrelator.get_displacement
.. automethod:: piv.fft_correlator.FFTCorrelator._evaluate_windows


