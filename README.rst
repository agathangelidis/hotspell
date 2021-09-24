""""""""
hotspell
""""""""

.....
About
.....

Hotspell is a Python package that detects past heat wave events using daily
weather station data of minimum and maximum air temperature. The user can choose
between a range of predefined threshold-based and percentile-based heat wave
indices or alternatively can define a full customizable index.

The main output of hotspell are the dates and characteristics of heat waves
found within the study period, stored in a pandas DataFrame. If selected by the
user, summary statistics (i.e. annual metrics) of the heat wave events are also
computed.

............
Installation
............

Required dependencies are:

- `NumPy <https://numpy.org/>`_
- `pandas <https://pandas.pydata.org/>`_

These packages should be installed beforehand, using the conda environment
management system that comes with the Anaconda/Miniconda Python distribution.

Then, hotspell can be installed from PyPI using pip:

.. code:: console

   pip install hotspell

............
Quick Start
............

1. Import the hotspell package

.. code:: python

    import hotspell

2. Choose the heat wave index CTX90PCT

.. code:: python

    index_name = "ctx90pct"
    hw_index = hotspell.index(name=index_name)

3. Set your data path of your CSV file

.. code:: python

    mydata = "my_data/my_file.csv"

The CSV file should include the following columns

- Year
- Month
- Day
- Tmin
- Tmax

in the above order, **without** a header line. Each day should be in a seperate 
line; missing days/lines are allowed.

For example:

+------+-----+-----+------+------+
| 1999 | 8   | 29  | 23.2 | 37.1 |
+------+-----+-----+------+------+
| 1999 | 8   | 31  | 24.1 | 37.7 |
+------+-----+-----+------+------+
| ...  | ... | ... | ...  | ...  |
+------+-----+-----+------+------+


4. Find the heat wave events

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

Hotspell is licensed under the BSD 3-clause license.
