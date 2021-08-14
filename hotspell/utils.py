from datetime import date

import numpy as np
import pandas as pd


def _compute_overall_mean(timeseries, summer_months):
    mean = _keep_only_summer(timeseries, summer_months).mean().round(1)[0]
    return mean


def _import_data(filename, var, years=None):
    """
    Read the weather data from a csv file into a DataFrame and preprocess them. 
    
    It requires specific columns to be included in the csv file. If `years` is
    set, it subsets the DataFrame by the given years.

    Parameters
    ----------
    filename : str or path object
        The path of the csv file that contains the weather data. It requires
        specific columns to be included in the csv file in a specific order.
    var : str, one of 'tmin', 'tmax'
        The meteorological variable to keep.
    years : tuple(int, int)

    Returns
    -------
    DataFrame
    """
    df = pd.read_csv(filename, header=None, index_col=None)
    df = _preprocess_data(df, var, years)

    return df


def _keep_only_summer(df, summer_months):
    """
    Keep only the summer period.

    Parameters
    ----------
    df : DataFrame
        It should have a DateTime Index.
    summer_months : tuple(int, int)

    Returns
    -------
    DataFrame
    """
    return df.loc[df.index.month.isin(summer_months)].copy()


def _keep_or_drop_year(df, max_missing_days_per_year):
    df_missing = df.isna().groupby(df.index.year).sum()
    df_missing.columns = ["missing_days"]
    df_keep = df_missing.iloc[
        np.where(df_missing["missing_days"] < max_missing_days_per_year)
    ]
    return df_keep


def _percent_of_days_to_days(days_percent, summer_months):
    if summer_months:
        months = list(summer_months)
    else:
        months = [*range(1, 13)]
    days = np.ceil(
        (days_percent * 0.01)
        * ((date(2020, months[-1] + 1, 1) - date(2020, months[0], 1)).days)
    )
    return days


def _preprocess_data(df, var, years):
    if var == "tmax":
        df = df.drop(columns=[3])
    elif var == "tmin":
        df = df.drop(columns=[4])
    df.columns = ["year", "month", "day", "var"]

    df["date"] = (
        df["year"].astype(str)
        + df["month"].astype(str).str.zfill(2)
        + df["day"].astype(str).str.zfill(2)
    )
    df = df[["date", "var"]]
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
    df.set_index("date", inplace=True)

    df.index.names = ["index"]

    if years is not None:
        df = df.loc[years[0] : years[-1]]

    return df
