from distutils.core import setup
from Cython.Build import cythonize
import numpy as np

#setup(
#  name = 'Constants',
#  ext_modules = cythonize("constants.pxd"),
#)

setup(
  name = 'Classes',
  ext_modules = cythonize("genome.pyx"),
  include_dirs=[np.get_include()]
)

setup(
  name = 'Classes',
  ext_modules = cythonize("animal.pyx"),
  include_dirs=[np.get_include()]
)

setup(
  name = 'Classes',
  ext_modules = cythonize("population.pyx"),
  include_dirs=[np.get_include()]
)

# setup(
#   name = 'Environment',
#   ext_modules = cythonize("environment.pyx"),
# )

setup(
  name = 'Main iterator',
  ext_modules = cythonize("iterate_population.pyx"),
  include_dirs=[np.get_include()]
)

setup(
  name = 'Main function',
  ext_modules = cythonize("main.pyx"),
  include_dirs=[np.get_include()]
)