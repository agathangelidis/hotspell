import datetime
from operator import add, sub
import os

import numpy as np
import pandas as pd

from .metrics import _get_annual_metrics
from .utils import _import_data, _keep_only_summer


class HeatWaves:
    """
    Class designed for storing heat wave events.

    It is the holder for the output of `get_heatwaves`.

    Parameters
    ----------
    events : DataFrame
        It contains the dates of detected heat wave events, as well as their
        basic characteristics (duration and temperature statistics).
    metrics : DataFrame
        It contains the summary of heat waves per year via standard metrics.
        Years with no heat waves are distinguished from years with missing
        data.

    Notes
    -----
    Column names of metrics correspond to:
    
    hwn : Heat wave number
        The annual total sum of heat wave events
    hwf : Heat wave day frequency
        The annual total sum of heat wave days
    hwd : Heat wave duration
        The length of the longest heat wave per year
    hwdm : Heat wave duration (mean)
        The average length of heat waves per year
    hwm : Heat wave magnitude
        The average magnitude of all events (anomaly against seasonal mean)
    hwma : Heat wave magnitude (absolute value)
        The average magnitude of all events
    hwa : Heat wave amplitude
        The hottest day of hottest event per year (anomaly against seasonal
        mean)
    hwaa : Heat wave amplitude (absolute value)
        The hottest day of hottest event per year
    """

    def __init__(self, events, metrics):
        self.events = events
        self.metrics = metrics


def get_heatwaves(
    filename,
    hw_index,
    ref_years=("1961-01-01", "1990-12-31"),
    summer_months=(6, 7, 8),
    max_missing_days_pct=10,
    export=True,
    metrics=True,
):
    """
    Detect heat wave events from weather station data.

    Parameters
    ----------
    filename : str or path object
        The path of the csv file that contains the weather data. It requires
        specific columns to be included in the csv file in a specific order.
    hw_index : HeatWaveIndex
        An HeatWaveIndex object created using the `index` function.
    ref_years : tuple of str, default ("1961-01-01", "1990-12-31")
        The first and the last year of the reference period. It should be set
        using the "YYYY-MM-DD" format.
    summer_months : tuple of int or None, default (6, 7, 8)
        A tuple with all months of the summer period. For the southern
        hemisphere it should be set as (12, 1, 2) or similar variants.
    max_missing_days_pct : int, default 10
        The percentage of maximum missing days for a year to be considered valid
        and be included in the metrics. If a summer period has been defined the
        percentage corresponds only to this period.
    export : bool, default True
        If True, output is exported as csv files in the same folder as the input
        data.
    metrics : bool, default True
        If True, annual metrics are computed and are exported if `export=True`.

    Returns
    -------
    HeatWaves object
     """
    timeseries = _import_data(filename=filename, var=hw_index.var)
    timeseries_ref_period = timeseries.loc[ref_years[0] : ref_years[-1]]

    daily_windows = _create_daily_windows(hw_index.window_length)

    daily_thresholds = _compute_daily_thresholds(
        daily_windows=daily_windows,
        timeseries_ref_period=timeseries_ref_period,
        hw_index=hw_index,
        summer_months=_extend_plus_minus_one_month(summer_months),
    )

    timeseries = _add_threshold_to_timeseries(timeseries, daily_thresholds)

    heatwaves = _find_heatwaves(
        timeseries=timeseries, hw_index=hw_index, summer_months=summer_months
    )

    if metrics is True:
        annual_metrics = _get_annual_metrics(
            heatwaves,
            timeseries_ref_period,
            timeseries,
            max_missing_days_pct,
            summer_months,
        )
    else:
        annual_metrics = None

    if export is True:
        _export_heatwaves(heatwaves, filename, hw_index.name)
        if metrics is True:
            _export_annual_metrics(annual_metrics, filename, hw_index.name)

    output = _create_output_object(heatwaves, annual_metrics)
    return output


def _create_daily_windows(window_length):
    """
    Add to each day  of the year a list of days within a window around this day.

    Parameters
    ----------
    window_length : int
        The length in days of the moving window, centered around a given day.

    Returns
    -------
    Dataframe
    """
    day_of_year = pd.date_range("1972-01-01", freq="D", periods=366)
    df = pd.DataFrame(index=day_of_year)

    days = np.floor(window_length / 2)
    df["after"] = _add_or_subtract_days(df.index, days, add)
    df["before"] = _add_or_subtract_days(df.index, days, sub)

    df["window"] = [
        pd.date_range(x, y).strftime("%m-%d").tolist()
        for x, y in zip(df["before"], df["after"])
    ]
    return df[["window"]]


def _add_or_subtract_days(ser, days, op):
    """
    Add or subtract a number of days.

    Parameters
    ----------
    ser : Series or Index
    days : int or float
    op : operator object, one of `add` or `sub` 

    Returns
    -------
    Series
    """
    return op(ser, datetime.timedelta(days))


def _extend_plus_minus_one_month(months):
    """
    Extend by one month a collection of months in both directions.

    Parameters
    ----------
    months : tuple of int

    Returns
    -------
    tuple of int
    """
    months = list(months)
    if months[0] == 1:
        months_extended = [12, *months, months[-1] + 1]
    elif months[-1] == 12:
        months_extended = [months[0] - 1, *months, 1]
    else:
        months_extended = [months[0] - 1, *months, months[-1] + 1]
    return tuple(sorted(months_extended))


def _compute_daily_thresholds(
    daily_windows, timeseries_ref_period, hw_index, summer_months
):
    """ 
    Compute per day a percentile-based threshold or set an absolute threshold.

    Parameters
    ----------
    daily_windows : DataFrame
        The output of `_create_daily_windows`.
    timeseries_ref_period : DataFrame
        The weather data for the reference period; they are used to calculated
        the percentile. 
    hw_index : HeatWaveIndex object
    summer_months : tuple of int

    Returns
    -------
    DataFrame
    """
    if summer_months:
        daily_thresholds = _keep_only_summer(
            daily_windows.copy(), summer_months
        )
    else:
        daily_thresholds = daily_windows.copy()

    if hw_index.pct is not None:
        timeseries_ref_period = timeseries_ref_period.set_index(
            timeseries_ref_period.index.strftime("%m-%d")
        )
        pct_values = []
        for window in daily_thresholds["window"]:
            pct_values.append(
                np.nanpercentile(
                    timeseries_ref_period.loc[
                        timeseries_ref_period.index.isin(window), "var"
                    ].values,
                    hw_index.pct,
                )
            )
        daily_thresholds["threshold"] = pct_values
    else:
        daily_thresholds["threshold"] = hw_index.fixed_thres

    daily_thresholds = daily_windows.join(daily_thresholds.drop("window", 1))
    return daily_thresholds


def _add_threshold_to_timeseries(timeseries, daily_thresholds):
    """Concatinate the station data and the computed daily thresholds."""
    timeseries = timeseries.asfreq("D")
    df = timeseries.assign(
        date=timeseries.index.strftime("%m-%d"),
        fulldate=timeseries.index.strftime("%Y-%m-%d"),
    ).merge(
        daily_thresholds.assign(
            date=daily_thresholds.index.strftime("%m-%d"), on="date"
        )
    )
    df = df.sort_values("fulldate").drop(
        ["date", "fulldate", "window"], axis=1
    )
    df.index = timeseries.index
    return df


def _find_heatwaves(timeseries, hw_index, summer_months):
    """
    Find the heat wave dates according to the criteria of a heat wave index.

    Parameters
    ----------
    timeseries : DataFrame
        The weather data including a column with a daily threshold value.
    hw_index : HeatWaveIndex object
    summer_months : tuple of int

    Returns
    -------
    DataFrame
    """
    timeseries["over"] = np.where(
        timeseries["var"] > timeseries["threshold"], 1, np.nan
    )

    if summer_months:
        timeseries = _keep_only_summer(timeseries, summer_months)

    heatwave_days = timeseries.copy()

    heatwaves = _group_heatwave_days(heatwave_days)
    heatwaves = _compute_heatwave_properties(
        heatwaves=heatwaves, var=hw_index.var
    )
    heatwaves = _filter_with_min_duration(heatwaves, hw_index.min_duration)

    return heatwaves


def _group_heatwave_days(heatwaves_days):
    heatwaves_days["group"] = (
        (heatwaves_days.over.diff(1) != 0).astype("int").cumsum()
    )
    return heatwaves_days


def _compute_heatwave_properties(heatwaves, var):
    heatwaves["date"] = heatwaves.index
    heatwaves_with_properties = pd.DataFrame(
        {
            "begin_date": heatwaves.groupby("group").date.first(),
            "end_date": heatwaves.groupby("group").date.last(),
            "duration": heatwaves.groupby("group").size(),
            f"avg_{var}": heatwaves.groupby("group")["var"].mean().round(1),
            f"std_{var}": heatwaves.groupby("group")["var"].std().round(1),
            f"max_{var}": heatwaves.groupby("group")["var"].max().round(1),
        }
    ).reset_index(drop=True)
    heatwaves_with_properties.index = pd.DatetimeIndex(
        heatwaves_with_properties.begin_date
    )
    heatwaves_with_properties.index.names = ["index"]
    return heatwaves_with_properties


def _filter_with_min_duration(heatwaves, min_duration):
    return heatwaves[heatwaves.duration >= min_duration]


def _export_heatwaves(heatwaves, filename, index_name):
    output_file = (
        f"{os.path.splitext(filename)[0]}_{index_name}_heatwaves_events.csv"
    )
    heatwaves.to_csv(output_file, index=False, date_format="%d/%m/%Y")


def _export_annual_metrics(metrics, filename, index_name):
    output_file = (
        f"{os.path.splitext(filename)[0]}_{index_name}_heatwaves_metrics.csv"
    )
    metrics.to_csv(output_file, index=True, date_format="%Y")


def _create_output_object(heatwaves, annual_metrics):
    output = HeatWaves(events=heatwaves, metrics=annual_metrics)
    return output
