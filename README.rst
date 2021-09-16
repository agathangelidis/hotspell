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
user.

Definitions and naming conventions for the indices and metrics follow `Perkins &
Alexander (2013) <https://doi.org/10.1175/JCLI-D-12-00383.1>`_.

............
Installation
............

Required dependencies are:

- `NumPy <https://numpy.org/>`_
- `pandas <https://pandas.pydata.org/>`_

These packages should be installed beforehand using the conda environment
management system that comes with the anaconda/miniconda python distribution.

Then, hotspell can be installed from PyPI using pip:

.. code:: console

   pip install hotspell

............
Quick Start
............

Import the hotspell package

.. code:: python

    import hotspell

Initialize the heat wave index CTX90PCT

.. code:: python

    index_name = "ctx90pct"
    hw_index = hotspell.index(name=index_name)

Set your data path

.. code:: python

    mydata = "my_data/my_file.csv"

Find the heat wave events

.. code:: python

    hw = hotspell.get_heatwaves(filename=mydata, hw_index=hw_index)
    heatwaves_events = hw.events
    heatwaves_metrics = hw.metrics 

................
Acknowledgements
................
Hotspell is developed during research under the Greek project *National Network
for Climate Change and its Impact*, `CLIMPACT <https://climpact.gr/main/>`_.

........
License
........
Hotspell is licensed under the BSD 3-clause licence.
