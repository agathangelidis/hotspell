import datetime
from operator import add, sub
import os

import numpy as np
import pandas as pd

from .metrics import _get_annual_metrics
from .utils import _import_data, _get_summer


def get_heatwaves(
    station,
    hw_index,
    ref_years=("1961-01-01", "1990-12-31"),
    summer_months=(6, 7, 8),
    export=True,
    metrics=True,
    max_missing_days_pct=5,
):
    daily_windows = _create_daily_windows(hw_index.window_length)

    timeseries_ref_period = _import_data(
        var=hw_index.var, station=station, years=ref_years
    )

    daily_thresholds = _compute_daily_thresholds(
        daily_windows=daily_windows,
        timeseries_ref_period=timeseries_ref_period,
        summer_months=_extend_plus_minus_one_month(summer_months),
        hw_index=hw_index,
    )

    timeseries = _import_data(var=hw_index.var, station=station)
    timeseries = _add_threshold_to_timeseries(timeseries, daily_thresholds)

    heatwaves = _find_heatwaves(timeseries)

    if summer_months:
        heatwaves = _get_summer(heatwaves, summer_months)

    heatwaves = _add_heatwave_properties(heatwaves=heatwaves, var=hw_index.var)

    heatwaves = _filter_with_min_duration(heatwaves, hw_index.min_duration)

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
        _export_heatwaves(heatwaves, station, hw_index.name)
        if metrics is True:
            _export_annual_metrics(annual_metrics, station, hw_index.name)

    return heatwaves, annual_metrics


def _create_daily_windows(window_length):
    """
    Constructs a dummy dataframe with n-days windows per calendar day.
    """
    day_of_year = pd.date_range("1972-01-01", freq="D", periods=366)
    df = pd.DataFrame(index=day_of_year)

    df["after"] = _add_or_subtract_days(df, window_length, add)
    df["before"] = _add_or_subtract_days(df, window_length, sub)

    df["window"] = [
        pd.date_range(x, y).strftime("%m-%d").tolist()
        for x, y in zip(df["before"], df["after"])
    ]
    return df[["window"]]


def _add_or_subtract_days(df, window_length, op):
    """
    Add/Subtract n days to each day of the year.
    df = input dataframe, window_length = window length in days, op = add/sub
    """
    return op(
        df.index.to_series(),
        datetime.timedelta(days=np.floor(window_length / 2)),
    )


def _compute_daily_thresholds(
    daily_windows, timeseries_ref_period, summer_months, hw_index
):
    if summer_months:
        daily_thresholds = _get_summer(daily_windows.copy(), summer_months)
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
        daily_thresholds["thres"] = pct_values
    else:
        daily_thresholds["thres"] = hw_index.fixed_thres

    daily_thresholds = daily_windows.join(daily_thresholds.drop("window", 1))
    return daily_thresholds


def _extend_plus_minus_one_month(months):
    months = list(months)
    if months[0] == 1:
        months_extended = [12, *months, months[-1] + 1]
    elif months[-1] == 12:
        months_extended = [months[0] - 1, *months, 1]
    else:
        months_extended = [months[0] - 1, *months, months[-1] + 1]
    return tuple(sorted(months_extended))


def _add_threshold_to_timeseries(timeseries, daily_thresholds):
    """
    Concatinates the derived threshold with the station data
    """
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


def _find_heatwaves(timeseries):
    """
    timeseries = the output of _add_threshold_to_timeseries()
    """
    timeseries["over"] = np.where(
        timeseries["var"] > timeseries["thres"], 1, np.nan
    )
    return timeseries


def _add_heatwave_properties(heatwaves, var):
    heatwaves["date"] = heatwaves.index.to_series()
    heatwaves["group"] = (heatwaves.over.diff(1) != 0).astype("int").cumsum()
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


def _export_heatwaves(heatwaves, station, index_name):
    output_file = f"{os.path.splitext(station)[0]}_{index_name}_heatwaves.csv"
    heatwaves.to_csv(output_file, index=False, date_format="%d/%m/%Y")


def _export_annual_metrics(metrics, station, index_name):
    output_file = (
        f"{os.path.splitext(station)[0]}_{index_name}_heatwaves_metrics.csv"
    )
    metrics.to_csv(output_file, index=True, date_format="%Y")
