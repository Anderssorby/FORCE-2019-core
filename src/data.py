import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('PS')
import matplotlib.pyplot as plt

"""
Read and prepare data
"""

def read_data():
    path = Path("data/Finalized")

    files = []

    for directory in path.glob("*"):
        for file in directory.glob("*.txt"):
            print(f"Reading {file}")
            df = pd.read_csv(file, sep="\t")
            files.append(df)

        # for file in directory.glob("*.las"):
        # print(f"Reading {file}")
        # las_file = read_las_file(str(file))
        # files.append(las_file)

    dfs = pd.concat(files, axis=0, join='outer', ignore_index=False, keys=None,
          levels=None, names=None, verify_integrity=False, copy=True)
    return dfs


def process_data(df):
    lithology_types = ["Sandstone", "Shale", "Mudstone", "Claystone", "Limestone"]

    grain_size_type = ["clay", "silt", "vf", "vf/f", "f", "f/m", "m", "m/c", "c",
            "c/vc", "vc", "vc/granule", "granule", "granule/pebble", "pebble"]
    gstl = len(grain_size_type)
    grain_size_value = [i/gstl for i, _ in enumerate(grain_size_type)]
    print(grain_size_value)
    # length = len(dframe["DEPTH"])
    # x_values = np.zeros((length, len(lithology_types)))
    top_name = "Grain_size_Top.-"
    base_name = "Grain_size_Base.-"
    top = None
    base = None

    change_points = []
    # fix grain_size data
    for i, row in df.iterrows():
        current_top = row[top_name]
        if current_top != top:
            # top changed
            if current_top not in grain_size_type:
                print("empty value")
                value = 0
            else:
                index = grain_size_type.index(current_top)
                value = grain_size_value[index]

            change_points.append((i, value))

            print(f"Top changed to:{row[top_name]} value: {value}")

            top = current_top
            base = row[base_name]

    df["grain_size"] = np.nan

    for i in range(1, len(change_points)):
        last_point, last_value = change_points[i-1]
        point, value = change_points[i]

        dif = (value-last_value)/(point-last_point)
        for row in range(last_point, point):
            df["grain_size"][row] = last_value + dif*(row-last_point)


    return df

#        for i in range(1, 4):
#            for j in range(1, 3):
#                l_type = dframe[f"LITHOLOGY{i}:{j}"]
#                ind = lithology_types.indexof(l_type)
#                x_values[row, 0] = ind

def string_to_float(a):
    return np.array([float(d) for d in a])



def plot_well(dframe):
    x = dframe["Depth.m"]
    # y = np.array([float(d[:-1]) for d in las["GR"]])
    y = dframe["GR.API"]

    plt.figure(1)
    plt.plot(x, y)
    plt.title("Plot")
    plt.legend(["Gamma Ray"])
    # plt.show()

    plt.savefig("figure.png")
    plt.close()


if __name__ == "__main__":
    data = read_data()

