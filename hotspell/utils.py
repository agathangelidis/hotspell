from datetime import date

import numpy as np
import pandas as pd


def _get_summer(df, summer_months=[*range(6, 9)]):
    "Keep summer months only."
    return df.loc[df.index.month.isin(summer_months)].copy()


def _import_data(var, station, years=None):
    "Imports the weather station data from a text file."
    df = pd.read_csv(station, sep=",", header=None, index_col=None)
    df = _preprocess_data(df, var)
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
    df.set_index("date", inplace=True)
    df.index.names = ["index"]
    if years is not None:
        df = df.loc[years[0] : years[-1]]

    return df


def _preprocess_data(df, var):
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
    return df[["date", "var"]]


def _pct_to_days(max_missing_days_per_year_pct, summer=True):
    if summer:
        months = [*range(6, 9)]
    else:
        months = [*range(1, 13)]
    max_missing_days_per_year = np.ceil(
        (max_missing_days_per_year_pct * 0.01)
        * ((date(2020, months[-1] + 1, 1) - date(2020, months[0], 1)).days)
    )
    return max_missing_days_per_year


def _keep_or_drop_year(df, max_missing_days_per_year):
    df_missing = df.isna().groupby(df.index.year).sum()
    df_missing.columns = ["missing_days"]
    df_keep = df_missing.iloc[
        np.where(df_missing["missing_days"] < max_missing_days_per_year)
    ]
    return df_keep
