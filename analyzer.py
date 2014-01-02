# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 12:13:23 2014

@author: damian
"""
import time
import datetime				#for converting string to epoch
from pandas import DataFrame, concat



timestampsQ, qbers, datasetQ = [], [], []
timestampsRaws, raws, datasetR = [], [], []

counter = -1
with open("rawlogs_measurements") as f:
    content = f.readlines()
    for lines in content:
        if "FIRMWARE_VERSION" in lines:
            counter = counter + 1
        if "QBER" in lines:
            splitted_line = lines.split(" ")
            time_in_epoch = time.mktime(datetime.datetime.strptime(splitted_line[0], "%Y-%m-%d-%H:%M:%S").timetuple())
            timestampsQ.append(time_in_epoch)
            qbers.append(splitted_line[7])
            datasetQ.append(counter)
        elif "RAW_KEY_EXCHANGE_RATE" in lines:
            splitted_line = lines.split(" ")
            time_in_epoch = time.mktime(datetime.datetime.strptime(splitted_line[0], "%Y-%m-%d-%H:%M:%S").timetuple())
            timestampsRaws.append(time_in_epoch)
            raws.append(splitted_line[7])
            datasetR.append(counter)

            
            
experiment_data_Qber = DataFrame({"Timestamp": timestampsQ, "Qber": qbers, "Dataset": datasetQ})
experiment_data_Qber = experiment_data_Qber.set_index("Timestamp")

experiment_data_Raw = DataFrame({"Timestamp": timestampsRaws, "Raw key": raws, "Dataset": datasetR})
experiment_data_Raw = experiment_data_Raw.set_index("Timestamp")

final_data = concat([experiment_data_Qber,experiment_data_Raw])

final_data = final_data.sort_index()

# after prepaired data, time to plot it:

for new_counter in range(counter+1):
    print new_counter