import numpy as np
import pandas as pd


def filter_dataframe_by_keeping_values(df, column_name, values, verbose=True):
    """Remove all rows that don't have a value in `values`"""
    mask = df[column_name].isin(values)
    return df.loc[mask]


def filter_dataframe_by_missing_numeric_value(df, column_name, verbose=True):
    """Remove all rows that have a missing value."""
    mask = pd.to_numeric(df[column_name], errors="coerce").isnull()
    if verbose:
        n_dropped = mask.sum()
        as_pct = np.floor(n_dropped / mask.size * 100)
        print(f"Dropped {n_dropped} entries ({as_pct}%).")
    return df.loc[~mask]


def digitize(series, n):
    """Digitize a series.

    If you have a lot of values (such as floats) and you only want to categorize them
    in groups, then it makes sense to digitize the data.
    """
    return pd.qcut(series, n, labels=np.arange(n))


def categorical_as_one_hot(series):
    """Convert a column `col` with categorical values to one-hot vectors."""
    return pd.get_dummies(pd.Categorical(series)).values

def closest_value(series, num):
    """Return index of the entry that is closest to `num`."""
    idx = series.sub(num).abs().idxmin()
    return idx
