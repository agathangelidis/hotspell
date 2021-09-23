import numpy as np
import pandas as pd

from .utils import (
    _compute_overall_mean,
    _keep_or_drop_year,
    _keep_only_summer,
    _percent_of_days_to_days,
)


def _get_annual_metrics(
    heatwaves,
    timeseries_ref_period,
    timeseries,
    max_missing_days_pct,
    summer_months,
):
    """
    Calculate the annual heat wave metrics attribute of a HeatWave object. 

    Parameters
    ----------
    heatwaves : HeatWave object
    timeseries_ref_period : DataFrame
    timeseries : DataFrame
    max_missing_days_pct : int
    summer_months : tuple of int

    Returns
    -------
    HeatWave object
    """
    ref_period_mean = _compute_overall_mean(
        timeseries_ref_period, summer_months
    )

    annual_metrics = _compute_annual_metrics(heatwaves, ref_period_mean)
    annual_metrics = _add_valid_years_with_no_heatwaves(
        annual_metrics, timeseries, max_missing_days_pct, summer_months
    )
    return annual_metrics


def _compute_annual_metrics(df, ref_period_mean):
    hwn = (
        df.groupby([df.index.year], as_index=True)["duration"]
        .count()
        .to_frame(name="hwn")
    )

    hwf = (
        df.groupby([df.index.year], as_index=True)["duration"]
        .sum()
        .to_frame(name="hwf")
    )

    hwd = (
        df.groupby([df.index.year], as_index=True)["duration"]
        .max()
        .to_frame(name="hwd")
    )

    hwdm = (
        df.groupby([df.index.year], as_index=True)["duration"]
        .mean()
        .to_frame(name="hwdm")
        .round(1)
    )

    hwm = (
        df.groupby([df.index.year], as_index=True)["max_tmax"]
        .mean()
        .to_frame(name="hwm")
        .round(1)
    )
    hwm["hwm"] = np.round(hwm["hwm"] - ref_period_mean, 1)

    hwma = (
        df.groupby([df.index.year], as_index=True)["max_tmax"]
        .mean()
        .to_frame(name="hwma")
        .round(1)
    )

    max_avg_tmax_dates = df.groupby([df.index.year], as_index=True)[
        "avg_tmax"
    ].transform(max)

    hwa = df[df["avg_tmax"] == max_avg_tmax_dates]["max_tmax"].to_frame(
        name="hwa"
    )
    hwa.index = hwa.index.year
    hwa["hwa"] = np.round(hwa["hwa"] - ref_period_mean, 1)

    hwaa = df[df["avg_tmax"] == max_avg_tmax_dates]["max_tmax"].to_frame(
        name="hwaa"
    )
    hwaa.index = hwaa.index.year

    annual_metrics = pd.concat(
        [hwn, hwf, hwd, hwdm, hwm, hwma, hwa, hwaa], axis=1
    )
    annual_metrics.index.rename("year", inplace=True)

    return annual_metrics


def _add_valid_years_with_no_heatwaves(
    metrics, timeseries, max_missing_days_pct, summer_months
):
    max_missing_days_per_year = _percent_of_days_to_days(
        max_missing_days_pct, summer_months
    )

    timeseries = timeseries.drop(columns=["threshold", "on", "over"])
    timeseries = _keep_only_summer(timeseries, summer_months)
    timeseries = _keep_or_drop_year(timeseries, max_missing_days_per_year)
    timeseries.index.name = "year"
    timeseries.rename(columns={"missing_days": "hwf"}, inplace=True)
    timeseries["hwf"] = 0
    timeseries["hwn"] = timeseries["hwf"]
    timeseries = timeseries.loc[~timeseries.index.isin(metrics.index)]

    metrics = pd.concat([metrics, timeseries]).sort_index(axis=0)
    return metrics
