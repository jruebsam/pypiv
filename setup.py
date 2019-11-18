#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy as np

ext_modules = [ Extension("pypiv.piv.interpolator", [ "pypiv/piv/interpolator.pyx" ])]
cmdclass = { }
cmdclass.update({ 'build_ext': build_ext })

setup(name='pypiv',
      version='0.01',
      description='Python Particle Image Velocimerty Library',
      author='Jonas Ruebsam',
      author_email='jonas.ruebsam@gmail.com',
      packages=['pypiv', 'pypiv.piv'],
      cmdclass=cmdclass,
      include_dirs = [np.get_include()],
      ext_modules=ext_modules,
     )
