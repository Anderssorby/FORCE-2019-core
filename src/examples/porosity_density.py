import numpy as np
import pandas as pd

"""
Load dataframe for porosity and density.

For the moment, just an example file. Some functionality will probably be moved
elsewhere at a later point.
"""

fname = "data/RealPore_Por_Perm_Lithology_data_1240_Wells_Norway_public.xlsx"
df = pd.read_excel(fname)

index_col = 0
dtype = {
    "Data source file name": str,
    "Well Name": str,
    "Measured Depth": float,
    "Permeability horizontal ka  (air) ": float,
    "Permeability vertical ka  (air) ": float,
    "porosity best of available": float,
    "gain density gr/cm3": float,
    "Formation description original": str,
    "main lithology": "category",
    "grain size": "category",
}
usecols = list(dtype.keys())
last_row = 134585
df = pd.read_excel(
    fname,
    sheet_name="Combined all wells",
    index_col=index_col,
    usecols=dtype.keys(),
    nrows=last_row,
)


def filter_dataframe_by_missing_numeric_value(df, column_name, verbose=True):
    mask = pd.to_numeric(df[column_name], errors="coerce").isnull()
    if verbose:
        n_dropped = mask.sum()
        as_pct = np.floor(n_dropped / mask.size * 100)
        print(f"Dropped {n_dropped} entries ({as_pct}%).")
    return df.loc[~mask]


filtered = filter_dataframe_by_missing_numeric_value(df, "Measured Depth")

for col in ["gain density gr/cm3", "Permeability vertical ka  (air) "]:
    print(col)
    filter_dataframe_by_missing_numeric_value(df, col)
