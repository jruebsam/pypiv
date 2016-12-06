import pyfftw
import numpy as np

from process import find_subpixel_peak
from process import find_subpixel_peak_2D

class FFTCorrelator(object):
    '''
    An FFT Correlation Class for a PIV Evaluation of two frames
    '''
    def __init__(self, window_a_size, window_b_size, scale_fft='default'):
        '''
        Initialize fftw objects for FFTs with the pyfftw library
        '''
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
        '''Set zero padding size for ffts'''
        if scale_fft == 'default':
            pad = 2*windows_size
        if scale_fft == 'upscale':
            pad =  2**np.ceil(np.log2(2*windows_size))
        return (pad, pad)

    def _evaluate_windows(self, window_a, window_b):
        fft_a = self._fa_fft(window_a - np.mean(window_a))
        fft_b = self._fb_fft(window_b - np.mean(window_b))

        fft_corr  = fft_a*np.conj(fft_b)
        inv_fft = self._ift_fft(fft_corr)
        #return np.fft.fftshift(inv_fft.real, axes=(0, 1))
        return np.fft.fftshift(inv_fft)

    def get_displacement(self, window_a, window_b):
        correlation = self._evaluate_windows(window_a, window_b)
        xi, yi = find_subpixel_peak(correlation, subpixel_method='gaussian')
        #xi, yi = find_subpixel_peak_2D(correlation)
        cx, cy = correlation.shape
        corr_pad = (window_b.shape[0] - window_a.shape[0])/2.
        return (cx/2. - xi - corr_pad, cy/2. - yi - corr_pad)

    def get_displacement_2D(self, window_a, window_b):
        correlation = self._evaluate_windows(window_a, window_b)
        #xi, yi = find_subpixel_peak(correlation, subpixel_method='gaussian')
        xi, yi = find_subpixel_peak_2D(correlation)
        cx, cy = correlation.shape
        corr_pad = (window_b.shape[0] - window_a.shape[0])/2.
        return (cx/2. - xi - corr_pad, cy/2. - yi - corr_pad)
