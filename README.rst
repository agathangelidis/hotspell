""""""""
hotspell
""""""""

Hotspell is a python package that detects past heat wave events using weather
station data. The user can choose between a range of different threshold-based
or percentile-based heatwave indices. Alternatively a custom index can be
defined.

The main output of hotspell is a Pandas DataFrame that includes the dates and
characteristics of all heat waves within the study period. Additionally,
summary statistics (annual metrics) can also be computed if selected by the
user. Naming conventions for the indices and metrics follow `Perkins &
Alexander (2013) <https://doi.org/10.1175/JCLI-D-12-00383.1>`_.

............
Installation
............

============
Requirements
============
Required dependencies are:

- `NumPy <https://numpy.org/>`_
- `pandas <https://pandas.pydata.org/>`_

These packages can be easily installed via the conda environment management
system that comes with the Anaconda/miniconda python distribution.

................
Acknowledgements
................
Hotspell is developed during research under the Greek project *National Network
for Climate Change and its Impact*, `CLIMPACT <https://climpact.gr/main/>`_.

........
License
........
Hotspell is licensed under the BSD 3-clause licence.
