import pytest
import os
import numpy as np

import pypiv.piv.process as process

@pytest.fixture(scope='module')

def data():
    script_path = os.path.dirname(os.path.realpath(__file__))
    file_path   = os.path.join(script_path, 'data/correlation.npy')
    window = np.load(file_path)
    return window

def test_1D_elliptical_gauss(data):
    xo, yo = process.find_subpixel_peak(data,subpixel_method='gaussian')
    assert abs(xo-31.5) < 0.01
    assert abs(yo-31.5) < 0.01

def test_2D_elliptical_gauss(data):
    xo, yo = process.find_subpixel_peak_2D(data)
    assert abs(yo-31.5) < 0.01
    assert abs(xo-31.5) < 0.01

