import os
import pkg_resources

import numpy as np
import pandas as pd

from hotspell.heatwaves import get_heatwaves
from hotspell.indices import index


def test_output_custom_index():
    station = pkg_resources.resource_filename(
        "hotspell", os.path.join("datasets", "test_input.csv"),
    )

    hw_index = index(var="tmax", pct=90, min_duration=3, window_length=3,)

    output, _ = get_heatwaves(
        station=station,
        hw_index=hw_index,
        ref_years=["1970-01-01", "1971-12-31"],
        export=False,
        metrics=False,
    )
    output = output.iloc[:, 2:].astype(float).values

    input_file = pkg_resources.resource_filename(
        "hotspell", os.path.join("datasets", "target_output.csv"),
    )
    target_output = pd.read_csv(
        input_file, sep=",", skiprows=1, header=None, index_col=False
    )
    target_output = target_output.iloc[:, 2:].astype(float).values

    assert np.array_equal(output, target_output) is True


def test_output_predefined_index():
    station = pkg_resources.resource_filename(
        "hotspell", os.path.join("datasets", "test_input.csv"),
    )

    index_name = "test_index"
    hw_index = index(name=index_name)

    output, _ = get_heatwaves(
        station=station,
        hw_index=hw_index,
        ref_years=["1970-01-01", "1971-12-31"],
        export=True,
        metrics=True,
        max_missing_pct=100,
    )
    output = output.iloc[:, 2:].astype(float).values

    input_file = pkg_resources.resource_filename(
        "hotspell", os.path.join("datasets", "target_output.csv"),
    )
    target_output = pd.read_csv(
        input_file, sep=",", skiprows=1, header=None, index_col=False
    )
    target_output = target_output.iloc[:, 2:].astype(float).values

    assert np.array_equal(output, target_output) is True
