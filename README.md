
Welcome to PyPIV!
=================


PyPIV is a python library for Particle Image Velocimetry (PIV), including pre and postprocessing functions.
For a closer look of the functionality take a look at the [official webpage](https://jr7.github.io/pypiv/ "PyPIV Homepage") of this library
where you can find the Documentation and Examples.

An installation of the [FFTW](http://www.fftw.org/) library is needed in order to use pypiv.

Install without PIP
-------------------

The installation can be performed directly from the git repository, a PIP package will be supported
in the future.

    git clone https://github.com/jr7/pypiv.git
    python setup.py build
    python setup.py install

Building PyPIV requires the following packages:

1. Python 3.7.x 
2. Numpy  1.19.x
3. SciPy  1.5.x
4. PyFFTW 0.12.x
5. Cython 0.29.x
6. scikit-image 0.17.x
7. matplotlib	3.3.x


Install with PIP
----------------

A setup.py file is provided for the installation with pip.
The required packages can be install with the setup.py or separately with the requierements.txt.
The separate installation of the packages can be performed by

	pip install -r requirements.txt

This step can be skipped if the installation is run with the setup.py by this command in the root directory of the repository

	pip install -e .

