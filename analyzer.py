# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 12:13:23 2014

@author: damian
"""
# to prevent window appear http://matplotlib.org/faq/howto_faq.html#generate-images-without-having-a-window-appear
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import time
import datetime				#for converting string to epoch
from pandas import DataFrame, concat


fresh_start = False

timestampsQ, qbers, datasetQ = [], [], []
timestampsRaws, raws, datasetR = [], [], []
initialTimestamps = []

counter = -1
with open("rawlogs_measurements") as f:
    content = f.readlines()
    for lines in content:
        if "FIRMWARE_VERSION" in lines:
            counter = counter + 1                  
            #print time_in_epoch
            fresh_start = True
        elif "LINE_LENGTH_MEASUREMENT_RESULTS" in lines and fresh_start:
            splitted_line = lines.split(" ")
            time_in_epoch = time.mktime(datetime.datetime.strptime(splitted_line[0], "%Y-%m-%d-%H:%M:%S").timetuple())
            initialTimestamps.append(time_in_epoch)
            print fresh_start
            fresh_start = False
        elif "QBER" in lines:
            splitted_line = lines.split(" ")
            time_in_epoch = time.mktime(datetime.datetime.strptime(splitted_line[0], "%Y-%m-%d-%H:%M:%S").timetuple())
            timestampsQ.append(time_in_epoch)
            qbers.append(float(splitted_line[7])*100)
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
    #print new_counter
    Qbers = final_data[(final_data["Dataset"]==new_counter) & (final_data["Qber"] > 0) ]
    x1 = Qbers.index.tolist()
    y1 = Qbers["Qber"].tolist()
    x1_average = DataFrame.mean(Qbers)["Qber"]
    x1_std_dev = DataFrame.std(Qbers)["Qber"]
    #prepairing proper time:
    x1[:] = [x - initialTimestamps[new_counter] for x in x1]
    
    Raws = final_data[(final_data["Dataset"]==new_counter) & (final_data["Raw key"] > 0) ]
    x2 = Raws.index.tolist()
    y2 = Raws["Raw key"].tolist()
    #x2_average = 2
    #x2_std_dev = 3
    #once again correcting counter:
    x2[:] = [x - initialTimestamps[new_counter] for x in x2]
    print x1[0], x2[0], initialTimestamps[new_counter]
    # Two subplots, the axes array is 1-d http://matplotlib.org/examples/pylab_examples/subplots_demo.html
    f, axarr = plt.subplots(2, sharex=True)
    axarr[0].grid()
    axarr[0].plot(x1, y1)
    #average and 3* deviations
    axarr[0].hlines(x1_average,x1[0],x1[-1])
    axarr[0].hlines(x1_average+3*x1_std_dev,x1[0],x1[-1])
    axarr[0].hlines(x1_average-3*x1_std_dev,x1[0],x1[-1])
    axarr[0].set_title('Sharing X axis')
    axarr[1].grid()
    axarr[1].plot(x2, y2)
    #axarr[1].hlines(x2_average,x2[0],x2[-1])
    #axarr[1].hlines(x2_average+3*x2_std_dev,x2[0],x2[-1])
    #axarr[1].hlines(x2_average-3*x2_std_dev,x2[0],x2[-1])
    f.set_size_inches(14.0719,4.7953) #for poster
    plt.savefig(str(new_counter)+'foo.eps')
    plt.clf()