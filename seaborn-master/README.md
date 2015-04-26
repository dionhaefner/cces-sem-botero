Seaborn: statistical data visualization
=======================================

<div class="row">
<a href=http://stanford.edu/~mwaskom/software/seaborn/examples/anscombes_quartet.html>
<img src="http://stanford.edu/~mwaskom/software/seaborn/_static/anscombes_quartet_thumb.png" height="135" width="135">
</a>

<a href=http://stanford.edu/~mwaskom/software/seaborn/examples/timeseries_from_dataframe.html>
<img src="http://stanford.edu/~mwaskom/software/seaborn/_static/timeseries_from_dataframe_thumb.png" height="135" width="135">
</a>

<a href=http://stanford.edu/~mwaskom/software/seaborn/examples/distplot_options.html>
<img src="http://stanford.edu/~mwaskom/software/seaborn/_static/distplot_options_thumb.png" height="135" width="135">
</a>    

<a href=http://stanford.edu/~mwaskom/software/seaborn/examples/regression_marginals.html>
<img src="http://stanford.edu/~mwaskom/software/seaborn/_static/regression_marginals_thumb.png" height="135" width="135">
</a>

<a href=http://stanford.edu/~mwaskom/software/seaborn/examples/violinplots.html>
<img src="http://stanford.edu/~mwaskom/software/seaborn/_static/violinplots_thumb.png" height="135" width="135">
</a>

</div>

Seaborn is a Python visualization library based on matplotlib. It provides a high-level interface for drawing attractive statistical graphics.


Documentation
-------------

Online documentation is available [here](http://stanford.edu/~mwaskom/software/seaborn/).

Examples
--------

The documentation has an [example gallery](http://stanford.edu/~mwaskom/software/seaborn/examples/index.html) with short scripts showing how to use different parts of the package. You can also check out the example notebooks:

- [Controlling figure aesthetics in seaborn](http://nbviewer.ipython.org/github/mwaskom/seaborn/blob/master/examples/aesthetics.ipynb)

- [Graphical representations of linear models](http://nbviewer.ipython.org/github/mwaskom/seaborn/blob/master/examples/linear_models.ipynb)

- [Visualizing distributions of data](http://nbviewer.ipython.org/github/mwaskom/seaborn/blob/master/examples/plotting_distributions.ipynb)

- [Plotting statistical timeseries data](http://nbviewer.ipython.org/github/mwaskom/seaborn/blob/master/examples/timeseries_plots.ipynb)

Citing
------

Seaborn can be cited using a DOI provided through Zenodo: [![DOI](https://zenodo.org/badge/doi/10.5072/zenodo.12710.png)](http://dx.doi.org/10.5072/zenodo.12710)


Dependencies
------------

- Python 2.7 or 3.3+

### Mandatory

- [numpy](http://www.numpy.org/)

- [scipy](http://www.scipy.org/)

- [matplotlib](http://matplotlib.sourceforge.net)

- [pandas](http://pandas.pydata.org/)

### Recommended

- [statsmodels](http://statsmodels.sourceforge.net/)

- [patsy](http://patsy.readthedocs.org/en/latest/)


Installation
------------

To install the released version, just do

    pip install seaborn

You may instead want to use the development version from Github, by running

    pip install git+git://github.com/mwaskom/seaborn.git#egg=seaborn


Testing
-------

[![Build Status](https://travis-ci.org/mwaskom/seaborn.png?branch=master)](https://travis-ci.org/mwaskom/seaborn)

To test seaborn, run `make test` in the source directory. This will run the
unit-test suite (using `nose`). It will also execute the example notebooks and
compare the outputs of each cell to the data in the stored versions. 


Development
-----------

https://github.com/mwaskom/seaborn

Please [submit](https://github.com/mwaskom/seaborn/issues/new) any bugs you encounter to the Github issue tracker.

License
-------

Released under a BSD (3-clause) license


Celebrity Endorsements
----------------------

"Those are nice plots" -Hadley Wickham
