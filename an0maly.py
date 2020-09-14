import pandas
from pathlib import Path
import argparse
import json
from datetime import datetime
import typing as T
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import statistics as stat



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
    
    print()
    print("Percent of bad data:  ", badcount*100/totalcount,"%")
    print("new temperature median:   ", stat.median(newtemp))
    print("new temperature variance:   ", stat.variance(newtemp))

    avrglab1 = stat.mean(newtemp)
    devlab1 = stat.stdev(newtemp)
    avrgclass1 = data['temperature']['class1'].mean()
    devclass1 = data['temperature']['class1'].std()
    avrgoffice = data['temperature']['office'].mean()
    devoffice = data['temperature']['office'].std()
    print()
    print("possible temperature bounds are")
    print("lab1:    ", avrglab1-3*devlab1,"C\N{DEGREE SIGN} and ", avrglab1+3*devlab1,"C\N{DEGREE SIGN}")
    print("class1:  ", avrgclass1-3*devclass1,"C\N{DEGREE SIGN} and ", avrgclass1+3*devclass1,"C\N{DEGREE SIGN}")
    print("office:  ", avrgoffice-3*devlab1,"C\N{DEGREE SIGN} and ", avrgoffice+3*devoffice,"C\N{DEGREE SIGN}")
    print()