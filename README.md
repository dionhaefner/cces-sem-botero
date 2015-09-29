# cces-sem-botero

Welcome to the simulation code based on the work of Botero et al., 2015. This is an open-source package, developed with Python, and was created during the seminary course "Chaotic, Complex and Evolving Systems" at Heidelberg University during summer of 2015.


### The Model

The implemented model was obtained from Botero et al., 2015:

> Carlos A. Botero, Franz J. Weissing, Jonathan Wright, and Dustin R. Rubenstein  
> *Evolutionary tipping points in the capacity to adapt to environmental change*  
> **PNAS**, 112 (1): 184-189, 2015.  
> http://www.pnas.org/content/112/1/184.full

Minor changes have been applied to the model in order to test its robustness. This code now fully supports multiple parallel environments and migration between them. To be precise, the following adjustments have been made to the model suggested by Botero et al.:

* Introduced support for multiple parallel environments between which migration takes place
* Additional environmental parameter `O` (constant offset)
* A scale function that diminishes the effect of genes on insulation for extreme values (currently logarithmical)
* New genes dubbed `m` and `ma` encoding the probability to (reversibly) migrate to another random environment
* Possibility to limit certain genes to a range of values


### Installation

You will need to have Python 2.7 or 3.x installed, along with the usual numerical packages like `NumPy`, `Matplotlib` and `Pandas`. Additionally, parts of the project are written in Cython, so you will need to have this library installed as well. A convenient way to get all this is [Anaconda Python](https://store.continuum.io/cshop/anaconda/), which is available for all major OS, and free of charge. Another highly recommended package that is not included with Anaconda Python is [Seaborn](https://www.stanford.edu/~mwaskom/software/seaborn/), which provides powerful tools of high-end data visualization. You can get this either from source or run

>	$ pip install seaborn

from your favorite Unix-style command line. Without Seaborn, all graphical output will be much less pretty, and violin plots are replaced by simple box plots.

If you cannot or do not want to install Anaconda Python, but have Python >= 2.7 and the package manager pip installed, you may run (with `sudo` as needed)

>	$ pip install -r requirements

in the main folder of this project. This should automatically install all the necessary requirements.

After you have installed the prerequisites, you will probably have to compile the Cython parts of the module once. To do this, execute

>	$ python setup.py build_ext --inplace

If none of the commands threw any errors you are ready to start simulating!


### Usage

The goal with this package was to create a software that is both easy to use and easy to modify. The simplest work flow for running simulations with this code would be:

1. Customize the model parameters in the file `constants.py`, as defined in the array `_PARAMETERS` (or just keep the default values).
2. Call `python main_constant.py` (simulation with constant population size), and grab a cup of coffee.
3. The output will be found in a new folder `output` and will contain the mean genes of the populations and their standard deviation in every time step, and a detailed plot every few time steps (may be specified in the `constants.py`).

For runs with variable population size, you also need to specify two `.csv`-files, containing the mean genes of the starting population and their standard deviation (output of a run with constant population size). You have to pass the name of these files via the command line.

For more usage examples consult the docs!


### Contact

Should you run into problems, do not hesitate to contact the author via e-mail:

mail@dionhaefner.de


### Legal

The project is licensed under the BSD 2-Clause License:

Copyright (c) 2015, Dion Häfner

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
