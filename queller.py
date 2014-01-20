# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 20:45:19 2014

@author: damian
"""
import matplotlib
matplotlib.use('Agg')
import os
import matplotlib.pyplot as plt
import time
import datetime				#for converting string to epoch
from pandas import DataFrame, concat

quelle_timestampsQ, quelle_qbers, quelle_datasetQ = [], [], []
quelle_timestampsRaws, quelle_raws, quelle_datasetR = [], [], []
quelle_initialTimestamps = []

file_counter = -1

data_in_next_line_qber = False
data_in_next_line_raw = False
 
path = '../quelle/'
listing = os.listdir(path)
for infile in listing:
    file_counter = file_counter + 1
    with open(path+infile) as f:
        content = f.readlines()
        splitted_line = content[0].split(" ")
        print splitted_line[0]
        time_in_epoch = time.mktime(datetime.datetime.strptime(splitted_line[0], "%Y-%m-%d_%H:%M:%S:").timetuple())
        quelle_initialTimestamps.append(time_in_epoch)        
        for lines in content:
            if "qber" in lines:
                data_in_next_line_qber = True
                continue
            elif "detector_counts_bob" in lines:
                data_in_next_line_raw = True
                continue
            if data_in_next_line_qber == True:
                if "uint" in lines:
                    data_in_next_line_qber = False
                    splitted_line = lines.split(" ")
                    value = int(splitted_line[9])
                    if value < 10000 and value > 0:
                        quelle_qbers.append(value/100.0)
                        quelle_datasetQ.append(file_counter)
                        time_in_epoch = time.mktime(datetime.datetime.strptime(splitted_line[0], "%Y-%m-%d_%H:%M:%S:").timetuple())
                        quelle_timestampsQ.append(time_in_epoch)
            elif data_in_next_line_raw == True:
                if "variant" in lines:
                    data_in_next_line_raw = False
                    splitted_line = lines.split(" ")
                    if len(splitted_line) == 10:                    
                        value = splitted_line[9]       
                        value = value.split(";")
                        if len(value) == 4:                  
                            #print int(value[0].replace('"','')),int(value[1]),int(value[2]),int(value[3].replace('"\n',''))
                            one_value = int(value[0].replace('"','')) + int(value[1]) + int(value[2]) + int(value[3].replace('"\n',''))
                            quelle_raws.append(one_value)
                            quelle_datasetR.append(file_counter)
                            time_in_epoch = time.mktime(datetime.datetime.strptime(splitted_line[0], "%Y-%m-%d_%H:%M:%S:").timetuple())
                            quelle_timestampsRaws.append(time_in_epoch)
                    

experiment_data_Qber = DataFrame({"Timestamp": quelle_timestampsQ, "Qber": quelle_qbers, "Dataset": quelle_datasetQ})
experiment_data_Qber = experiment_data_Qber.set_index("Timestamp")

experiment_data_Raw = DataFrame({"Timestamp": quelle_timestampsRaws, "Raw key": quelle_raws, "Dataset": quelle_datasetR})
experiment_data_Raw = experiment_data_Raw.set_index("Timestamp")

final_data = concat([experiment_data_Qber,experiment_data_Raw])

final_data = final_data.sort_index()

# after prepaired data, time to plot it:

for new_counter in range(file_counter+1):
    #print new_counter
    Qbers = final_data[(final_data["Dataset"]==new_counter) & (final_data["Qber"] > 0) ]
    x1 = Qbers.index.tolist()
    y1 = Qbers["Qber"].tolist()
    x1_average = DataFrame.mean(Qbers)["Qber"]
    x1_std_dev = DataFrame.std(Qbers)["Qber"]
    #prepairing proper time:
    x1[:] = [x - quelle_initialTimestamps[new_counter] for x in x1]
    
    Raws = final_data[(final_data["Dataset"]==new_counter) & (final_data["Raw key"] > 0) ]
    x2_average = DataFrame.mean(Raws)["Raw key"]
    x2_median = DataFrame.median(Raws)["Raw key"]
    x2_max = DataFrame.max(Raws)["Raw key"]
    
    Raws = Raws[Raws["Raw key"]<(x2_max - (x2_max/100)*20)]
    
    x2 = Raws.index.tolist()
    y2 = Raws["Raw key"].tolist()

    print x2_average
    #x2_std_dev = 3
    #once again correcting counter:
    x2[:] = [x - quelle_initialTimestamps[new_counter] for x in x2]
    #print x1[0], x2[0], quelle_initialTimestamps[new_counter]
    # Two subplots, the axes array is 1-d http://matplotlib.org/examples/pylab_examples/subplots_demo.html
    f, axarr = plt.subplots(2, sharex=True)
    axarr[0].grid()
    axarr[0].plot(x1, y1)
    #average and 3* deviations
    #axarr[0].hlines(x1_average,x1[0],x1[-1])
    #axarr[0].hlines(x1_average+3*x1_std_dev,x1[0],x1[-1])
    #axarr[0].hlines(x1_average-3*x1_std_dev,x1[0],x1[-1])
    axarr[0].set_title('Sharing X axis')
    axarr[1].grid()
    axarr[1].plot(x2, y2)
    #axarr[1].hlines(x2_average,x2[0],x2[-1])
    #axarr[1].hlines(x2_average+3*x2_std_dev,x2[0],x2[-1])
    #axarr[1].hlines(x2_average-3*x2_std_dev,x2[0],x2[-1])
    f.set_size_inches(14.0719,4.7953) #for poster
    plt.savefig("quelle"+ str(new_counter)+'foo.eps')
    plt.clf()