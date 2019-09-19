import pandas as pd
import pathlib
from collections import defaultdict
from src.pandas_tricks import closest_value


def get_grain_size_attribute(df, name="grain_size"):
    grain_size_mapping = {
        "clay": "clay",
        "silt": "silt",
        "very fine": "very fine grained",
        "very fine/fine": "fine grained very fine grained, very fine grained fine grained",
        "fine": "fine grained",
        "fine-medium": "conglomerate fine grained medium grained, medium fine grained, fine grained medium grained",
        "medium": "medium medium grained, medium grained",
        "medium-coarse": "medium very coarse grained, medium coarse grained ",
        "coarse": "coarse grained",
        "coarse ": "very coarse",
        "very coarse": "very coarse grained",
        "very coarse – granule": "conglomerate medium grained",
        "granule": "granule",
        "granule/pebble": "fine grained pebble",
        "pebble": "pebble",
    }
    grain_size_mapping = {k: v.split(", ") for (k, v) in grain_size_mapping.items()}
    inverse_grain_size_mapping = defaultdict(lambda: None)
    for k, v in grain_size_mapping.items():
        for item in v:
            inverse_grain_size_mapping[item] = k
    grain_sizes = df["grain size"].apply(lambda elem: inverse_grain_size_mapping[elem])
    return pd.Series(grain_sizes, name=name)


def get_sorting_attribute(df, name="sorting"):
    """Extract sorting attribute from DataFrame.

    We also do some renamings in the DataFrame
    """
    series = pd.Series(df["sorting"], name=name)
    replacements = {
        "sorted well sorted": "well sorted",
        "sorted fair sorted": "well sorted",
        "sorted moderate": "sorted",
        "medium sorted": "sorted",
        "very well sorted": "well sorted",
        "sorted fair sorted": "well sorted",
    }
    series = series.map(lambda k: k if k not in replacements else replacements[k])
    return series


def get_gamma_attribute(df, name="GR"):
    """Extract gamma rays for plugs.

    All LAS files are located under 'data/Finalized'. We can't use Lasio because it only
    supports LAS2 format, whereas the files we have available is in LAS3. We therefore
    only use the .txt files and parse the necessary columns (+ some more..) ourselves.

    The method can probably be made faster, but it works. :-)
    """
    p = pathlib.Path("data/Finalized")
    gamma_rays = pd.Series(index=df.index.values, name=name)
    for (well_name, depth), g in df.groupby(["Well Name", "Measured Depth"]):
        directories = list(p.glob(f"*_{well_name}"))
        assert len(directories) == 1, directories
        f = next(directories[0].glob("*.txt"))
        las = pd.read_csv(
            f,
            sep="\t",
            usecols=[
                "Depth.m",
                "GR.API",
                "Lithology1.-",
                "Lithology2.-",
                "Lithology3.-",
            ],
        )

        idx = closest_value(las["Depth.m"], depth)

        gamma_rays.loc[g.index] = las.loc[idx, "GR.API"]
    return gamma_rays.astype(float)


def get_porosity_attribute(df, name="porosity"):
    return pd.Series(df["porosity best of available"], name=name).astype(float)


def get_permeability_attribute(df, name="permeability"):
    # from discussions, we want to search for the following columns, in order:
    priority = [
        "Nitrogen Permeability. Hor.",
        "Nitrogen Permeability. Vert.",
        "Klinkenberg corrected gas perm. Hor.",
        "Klinkenberg corrected gas perm. Vert.",
        "Permeability horizontal ke  (klinkenberg corrected)  also called kl. KL",
    ]
    permeability = df[priority[0]]
    for col in priority[1:]:
        mask = permeability.isnull()
        print(mask.mean())
        print(df.loc[mask, col].isnull().all())
        permeability.loc[mask] = df.loc[mask, col]
    return pd.Series(permeability, name=name).astype(float)


def get_lithology_attribute(df, name="lithology"):
    lithologies = (
        df["main lithology"]
        .str.lower()
        .apply(lambda s: s if pd.isnull(s) else s.split(" ")[0])
    )
    return pd.Series(lithologies, name=name).astype(str)
