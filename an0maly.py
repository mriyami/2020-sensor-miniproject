import pandas
from pathlib import Path
import argparse
import json
from datetime import datetime
import typing as T
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from statistics import mean
from statistics import variance
from statistics import median


def load_data(file: Path) -> T.Dict[str, pandas.DataFrame]:

    temperature = {}
    occupancy = {}
    co2 = {}

    with open(file, "r") as f:
        for line in f:
            r = json.loads(line)
            room = list(r.keys())[0]
            time = datetime.fromisoformat(r[room]["time"])

            temperature[time] = {room: r[room]["temperature"][0]}
            occupancy[time] = {room: r[room]["occupancy"][0]}
            co2[time] = {room: r[room]["co2"][0]}

    data = {
        "temperature": pandas.DataFrame.from_dict(temperature, "index").sort_index(),
        "occupancy": pandas.DataFrame.from_dict(occupancy, "index").sort_index(),
        "co2": pandas.DataFrame.from_dict(co2, "index").sort_index(),
    }

    return data


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="load and analyse IoT JSON data")
    p.add_argument("file", help="path to JSON data file")
    P = p.parse_args()

    file = Path(P.file).expanduser()

    data = load_data(file)

    deviation = data['temperature']['lab1'].std()
    mean = data['temperature']['lab1'].mean()

    rows, col = data['temperature'].shape
    newtemp = []
    badcount = 0
    totalcount = 0

    for x in range(rows-1):
        if data['temperature']['lab1'][x] is None:
            pass 
        elif data['temperature']['lab1'][x] > (2*deviation+mean) or data['temperature']['lab1'][x] < (mean-2*deviation): 
            badcount += 1  
            totalcount += 1 
        else:
            newtemp.append(data['temperature']['lab1'][x])
            totalcount += 1 

    newtemp = [x for x in newtemp if np.isnan(x) == False]
    print("Percent of bad data:  ", badcount*100/totalcount,"%")
    print("new temperature median:   ", median(newtemp))
    print("new temperature variance:   ", variance(newtemp))


