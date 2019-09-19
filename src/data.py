import pandas as pd
import pathlib
import re
import numpy as np
from pathlib import Path
import matplotlib
from tqdm import tqdm

matplotlib.use("PS")
import matplotlib.pyplot as plt

"""
Read and prepare data
"""


def read_data():
    path = Path("data/Finalized")

    files = []
    names = []

    for directory in path.glob("*"):
        for file in directory.glob("*.txt"):
            print(f"Reading {file}")
            df = pd.read_csv(file, sep="\t")
            files.append(df)
            names.append(file.name)

        # for file in directory.glob("*.las"):
        # print(f"Reading {file}")
        # las_file = read_las_file(str(file))
        # files.append(las_file)

    dfs = pd.concat(files, axis=0, join="outer", ignore_index=False, names=names)
    return dfs


def process_data(df):
    lithology_types = ["Sandstone", "Shale", "Mudstone", "Claystone", "Limestone"]

    grain_size_type = [
        "clay",
        "silt",
        "vf",
        "vf/f",
        "f",
        "f/m",
        "m",
        "m/c",
        "c",
        "c/vc",
        "vc",
        "vc/granule",
        "granule",
        "granule/pebble",
        "pebble",
    ]

    gstl = len(grain_size_type)
    grain_size_value = [i / gstl for i, _ in enumerate(grain_size_type)]
    print(grain_size_value)
    # length = len(dframe["DEPTH"])
    # x_values = np.zeros((length, len(lithology_types)))
    top_name = "Grain_size_Top.-"
    base_name = "Grain_size_Base.-"
    top = None
    base = None

    change_points = []
    # fix grain_size data
    for i, row in tqdm(df.iterrows()):
        current_top = row[top_name]
        if current_top != top:
            # top changed
            if current_top not in grain_size_type:
                # print("empty value")
                value = np.nan
            else:
                index = grain_size_type.index(current_top)
                value = grain_size_value[index]

            change_points.append((i, value))

            # print(f"Top changed to:{row[top_name]} value: {value}")

            top = current_top
            base = row[base_name]

    df["grain_size"] = np.nan

    for i in tqdm(range(1, len(change_points))):
        last_point, last_value = change_points[i - 1]
        point, value = change_points[i]

        dif = (value - last_value) / (point - last_point)
        for row in range(last_point, point):
            df["grain_size"][row] = last_value + dif * (row - last_point)


def string_to_float(a):
    return np.array([float(d) for d in a])


def plot_well(df, key="GR.API"):
    x = df["Depth.m"]

    if isinstance(df[key][0], str):
        y = np.array([float(d[:-1]) for d in df[key]])
    else:
        y = df[key]

    df = df[df[key] == np.nan]

    plt.figure(1)
    plt.plot(x, y)
    plt.title(f"Plot of {key}")
    plt.legend([key])
    # plt.show()

    plt.savefig(f"{key}.png")
    plt.close()


def find_available_core_images():
    """Get a pd.DataFrame with info about each available core image samlpe.

    Returns:
        a pd.DataFrame with the following columns:
        - license: str, the license number of the well
        - well_no: str, the well number. License and well number uniquely identifies
            the well.
        - top: float; the top of the core sample
        - base: float; the base of the core sample
        - path: float; the path to the core sample image
    """
    data = []
    for f in pathlib.Path("data/logimages/").glob("**/*.jpg"):
        image_name = f.name
        m = re.match(
            r"(\d+)_(\d+_\d+)_(?:S_)?(\d+(?:[,.]\d+)?)_(\d+(?:[,.]\d+)?)\.jpg",
            image_name,
        )
        if m is None:
            print(f"Didnt parse {image_name}")
            continue
        license, well_no, top, base = m.groups()
        top, base = float(top.replace(",", ".")), float(base.replace(",", "."))
        data.append([license, well_no, top, base, image_name])
    return pd.DataFrame(data, columns=["license", "well_name", "top", "base", "path"])


def get_data():
    data = read_data()
    process_data(data)
    return data


def plot_data(data):
    plot_well(data, "GR.API")
    plot_well(data, "grain_size")


if __name__ == "__main__":
    data = get_data()
    plot_data(data)

