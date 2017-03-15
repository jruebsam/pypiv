import pyfftw
import numpy as np

from peak_detection import find_peak

class FFTCorrelator(object):
    """
    An FFT Correlation Class for a PIV Evaluation of two frames
    It uses the `pyfftw <https://hgomersall.github.io/pyFFTW/>`_ library for performant FFT.
    This class is also responsible for calculating the Shift after the correlation.
    """

    def __init__(self, window_a_size, window_b_size, scale_fft='default'):
        """
        Initialize fftw objects for FFTs with the pyfftw library

        The necessary functions are loaded and memory allocated.

        :param window_a_size: size of the interrogation window
        :param window_b_size: size of the search window
        :param str scale_fft: if set to upscale, the padding will be upscaled
        """
        max_fsize = max([window_a_size, window_b_size])
        pad = self._set_padding(max_fsize, scale_fft)

        ffta_shape     = (window_a_size, window_a_size)
        ffta_memory    = pyfftw.empty_aligned(ffta_shape, dtype='float64')
        self._fa_fft   = pyfftw.builders.rfft2(ffta_memory, pad)

        fftb_shape     = (window_b_size, window_b_size)
        fftb_memory    = pyfftw.empty_aligned(fftb_shape, dtype='float64')
        self._fb_fft   = pyfftw.builders.rfft2(fftb_memory, pad)

        ifft_shape     = (window_b_size, window_b_size//2 + 1)
        ifft_memory    = pyfftw.empty_aligned(ifft_shape, dtype='complex128')
        self._ift_fft  = pyfftw.builders.irfft2(ifft_memory, pad)

    def _set_padding(self, windows_size, scale_fft):
        """Set zero padding size for FFTs"""
        if scale_fft == 'default':
            pad = 2*windows_size
        if scale_fft == 'upscale':
            pad =  2**np.ceil(np.log2(2*windows_size))
        return (pad, pad)

    def _evaluate_windows(self, window_a, window_b):
        """
        Calculate the FFT of both windows, correlate and transform back.

        In order to decrease the error a mean subtraction is performed.
        To compensate for the indexing during the FFT a FFT Shift is performed.

        :param window_a: interrogation window
        :param window_b: search window
        :returns: correlation window
        """
        fft_a = self._fa_fft(window_a - np.mean(window_a))
        fft_b = self._fb_fft(window_b - np.mean(window_b))

        fft_corr  = fft_a*np.conj(fft_b)
        inv_fft = self._ift_fft(fft_corr)
        return np.fft.fftshift(inv_fft)

    def get_displacement(self, window_a, window_b, subpixel_method='gaussian'):
        """
        Compute the displacement out of correlation.

        First the correlation is performed and afterwards the shift is calculated.
        For the displacement calculation the function

        .. autofunction:: piv.peak_detection.find_peak

        is called with the subpixel_method passed on as parameter.
        If a padding was needed, it is removed from the calculated displacement.

        :param window_a: interrogation window
        :param window_b: search window
        :param str subpixel_method: method for peak finder
        :returns: shift in x and y direction as tuple
        """
        correlation = self._evaluate_windows(window_a, window_b)
        xi, yi = find_peak(correlation, subpixel_method)
        cx, cy = correlation.shape
        corr_pad = (window_b.shape[0] - window_a.shape[0])/2.
        return (cx/2. - xi - corr_pad, cy/2. - yi - corr_pad)

