import time
import datetime				#for converting string to epoch
from pandas import Series, DataFrame

timestamps, qbers = [], []

with open("rawlogs_measurements") as f:
    content = f.readlines()
    for lines in content:
        if "QBER" in lines:
			splitted_line = lines.split(" ")
			time_in_epoch = time.mktime(datetime.datetime.strptime(splitted_line[0], "%Y-%m-%d-%H:%M:%S").timetuple())
			timestamps.append(time_in_epoch)
			qbers.append(splitted_line[7])

experiment_data = DataFrame({"Timestamp": timestamps, "Qber": qbers})
experiment_data = experiment_data.set_index("Timestamp")
