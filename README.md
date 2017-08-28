
Welcome to PyPIV!
=================


PyPIV is a python library for Particle Image Velocimetry (PIV), including pre and postprocessing functions.
For a closer look of the functionality take a look at the [official webpage](https://jr7.github.io/pypiv/ "PyPIV Homepage") of this library
where you can find the Documentation and Examples.

Install
-------

The installation can be performed directly from the git repository, a PIP package will be supported
in the future.

    git clone https://github.com/jr7/pypiv.git
    python setup.py build
    python setup.py install

Building PyPIV requires the following software installed:

1. Python 2.7.x currently this library is only supported on Python 2.7.x support for Python 3.x will come in the future.
2. Numpy  1.12.x
3. SciPy  0.18.0
4. PyFFTW 0.10.3
5. Cython 0.23.4 optional for the use of cubic interpolation in window deformation methods
