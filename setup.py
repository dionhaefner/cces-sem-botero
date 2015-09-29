#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
#########################################################
#
#	setup.py
#	Author: Dion Häfner (dionhaefner@web.de)
#	
#	Compiles and builds cython modules of the project.
#	Needs to be called any time animal.pyx is changed.
#
#	Usage:
#		sudo python setup.py build_ext --inplace
#
#	Licensed under BSD 2-Clause License
#
#########################################################
"""

from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    name = "Enhanced Botero model cython functions",
    ext_modules = cythonize(['src/animal.pyx'],include_path=['./src/']),
    include_dirs=[numpy.get_include()]
) 
