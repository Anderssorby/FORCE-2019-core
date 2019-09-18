import pandas as pd
import numpy as np
import lasio
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


def read_las_file(file):
    try:
        las = lasio.read(file)
    except ValueError as e:
        las = None
        print(e)

    # breakpoint()

    return las

def process_file(las):
    lithology_types = ["Sandstone", "Shale", "Mudstone", "Claystone", "Limestone"]

    length = len(las["DEPTH"])
    x_values = np.zeros((length, len(lithology_types)))
    for row in range(length):
        for i in range(1, 4):
            for j in range(1, 3):
                l_type = las[f"LITHOLOGY{i}:{j}"]
                ind = lithology_types.indexof(l_type)
                x_values[row, 0] = ind

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

if __name__== "__main__":
    files = read_data()

