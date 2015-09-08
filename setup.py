from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    name = "Enhanced Botero model cython functions",
    ext_modules = cythonize(['src/animal.pyx'],include_path=['./src/']),
    include_dirs=[numpy.get_include()]  # accepts a glob pattern
) 
