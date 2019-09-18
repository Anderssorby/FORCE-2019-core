import pandas as pd
import numpy as np
import lasio
from pathlib import Path


def read_data():
    path = Path("data/Finalized")
    
    for directory in path.glob("*"):
        for file in directory.glob("*.las"):
            print(f"Reading {file}")
            res = read_las_file(str(file))
            print(res)



def read_las_file(file):
    return lasio.read(file)


if __name__== "__main__":
    read_data()
