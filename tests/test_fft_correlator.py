import pytest
import os
import numpy as np

from pypiv import FFTCorrelator

@pytest.fixture(scope='module')
def data():
    script_path = os.path.dirname(os.path.realpath(__file__))
    file_path   = os.path.join(script_path, 'data/center_particle.npy')
    window = np.load(file_path)
    size = window.shape[0]
    fft_corr = FFTCorrelator(window_a_size=size, window_b_size=size)
    return (fft_corr, window)

def test_zero_displacement(data):
    fft_corr, window = data
    assert fft_corr.get_displacement(window, window) == (0, 0)

def test_x_displacement(data):
    fft_corr, window_a = data
    window_b = np.roll(window_a, shift=4, axis=0)
    dx, dy = fft_corr.get_displacement(window_a, window_b)
    assert abs(dx - 4) < 0.01
    assert abs(dy)     < 0.01

def test_y_displacement(data):
    fft_corr, window_a = data
    window_b = np.roll(window_a, shift=4, axis=1)
    dx, dy =  fft_corr.get_displacement(window_a, window_b)
    assert abs(dx)      < 0.01
    assert abs(dy - 4)  < 0.01

def test_xy_displacement(data):
    fft_corr, window_a = data
    window_b = np.roll(window_a, shift=4, axis=0)
    window_b = np.roll(window_b, shift=4, axis=1)
    dx, dy =  fft_corr.get_displacement(window_a, window_b)
    assert abs(dx - 4)  < 0.01
    assert abs(dy - 4)  < 0.01

def test_xy_displacement2(data):
    fft_corr, window_a = data
    window_b = np.load('data/shift05.npy')
    #window_a = np.copy(window_b)
    #window_b = np.roll(window_b, shift=1, axis=0)
    #window_b = np.roll(window_b, shift=1, axis=1)
    dx, dy =  fft_corr.get_displacement(window_a, window_b)
    delta = .5
    assert abs(dx - delta)  < 0.01
    assert abs(dy - delta)  < 0.01
