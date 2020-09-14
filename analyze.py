#!/usr/bin/env python3
"""
This example assumes the JSON data is saved one line per timestamp (message from server).

It shows how to read and process a text file line-by-line in Python, converting JSON fragments
to per-sensor dictionaries indexed by time.
These dictionaries are immediately put into Pandas DataFrames for easier processing.

Feel free to save your data in a better format--I was just showing what one might do quickly.
"""
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

    #data["temperature"].plot()
    #time = data["temperature"].index

    #data["temperature"].hist()

    #plt.figure()
    #plt.hist(np.diff(time.values).astype(np.int64) // 1000000000)
    #plt.xlabel("Time (seconds)")

    print("Median temperature for each room")
    print("class1:   " , data['temperature']['class1'].median())
    print("lab1:     " ,data['temperature']['lab1'].median())
    print("office:   " ,data['temperature']['office'].median())
    print()
    print("Variance in temperature for each rooms")
    print("class1:   " ,data['temperature']['class1'].var())
    print("lab1:     " ,data['temperature']['lab1'].var())
    print("office:   " ,data['temperature']['office'].var())
    print()
    print("Median occupancy for each room")
    print("class1:   " , data['occupancy']['class1'].median())
    print("lab1:     " ,data['occupancy']['lab1'].median())
    print("office:   " ,data['occupancy']['office'].median())
    print()
    print("Variance in occupancy for each rooms")
    print("class1:   " ,data['occupancy']['class1'].var())
    print("lab1:     " ,data['occupancy']['lab1'].var())
    print("office:   " ,data['occupancy']['office'].var())
    print()


#one of many failed attempts at plotting PDF

#data['temperature']['lab1'].hist(bins=3000, density= True)
#n, x, _ = plt.hist(data['temperature']['lab1'], bins=np.linspace(-300, 50, 5), 
#          histtype=u'step', density=True) 
#sns.set_style('whitegrid')
#sns.kdeplot(np.array(data['temperature']['lab1']))
#sns.displot(np.array(data['temperature']['lab1']),range = (-50,50), kde=True)
#g = sns.FacetGrid(data['temperature'], col = 3)


#Creat and plot PDF:
fig1, axs = plt.subplots(1, 3,figsize=(9,6))
fig1.suptitle('PDF of Sensor Values in lab1', fontsize=16)
sns.histplot(np.array(data['temperature']['lab1']), stat = 'density', ax = axs[0], kde = True)
sns.histplot(np.array(data['occupancy']['lab1']), stat = 'density', discrete = True, ax = axs[1], kde = True)
sns.histplot(np.array(data['co2']['lab1']), stat = 'density', ax = axs[2], kde = True)
axs[1].set_ylabel('')
axs[2].set_ylabel('')
axs[0].set_xlabel('temperature')
axs[1].set_xlabel('occupancy')
axs[2].set_xlabel('co2')
plt.tight_layout() 


#Getting time intervals and plotting the PDF
rows, col = data['temperature'].shape
delta = []
for x in range(rows-1):
    delta.append(pandas.Timedelta(data['temperature'].index.array[x+1] - data['temperature'].index.array[x]).total_seconds())

print("Mean value of the time interval between two sensor readings is")
print(mean(delta))
print("Variance of the time interval is")
print(variance(delta))
print()

fig2, ax = plt.subplots(figsize=(9,6))
sns.histplot(delta, stat = 'density', bins = 100)
sns.kdeplot(data = delta, bw_adjust = 0.2, color = 'r')
ax.set_ylabel('Propability Density')
ax.set_xlabel('Time Interval')
fig2.suptitle('PDF of Time Interval Between Sensor Readings', fontsize = 16)
plt.tight_layout() 
print('The time interval plot mimics a plot of exponential decay, the longer the interval the less likely for it to occure')
print()

plt.show()