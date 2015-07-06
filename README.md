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


### Installation

You will need to have Python 2.7 or 3.x installed, along with the usual numerical packages like `NumPy`, `Matplotlib` and `Pandas`. A convenient way to get all this is [Anaconda Python](https://store.continuum.io/cshop/anaconda/), which is available for all major OS, and free of charge. Another highly recommended package that is not included with Anaconda Python is [Seaborn](https://www.stanford.edu/~mwaskom/software/seaborn/), which provides powerful tools of high-end data visualization. You can get this either from source or run

>	$ pip install seaborn

from your favorite Unix-style command line.


### Usage

Just clone the repository and execute `botero.py` in the main folder! You can also call `main_constant.py` and `main_variable.py` from command line, e.g. if you want to include these into a shell script that runs simulations autonomously. The model parameters can be changed in the file `constants.py`.

Examples for the usage of the custom classes are found in the file `example.py`.


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