# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 20:45:19 2014

@author: damian
"""

import os
import matplotlib.pyplot as plt

qbers_quelle = [] 
data_in_next_line = False
 
path = '../quelle/'
listing = os.listdir(path)
for infile in listing:
    with open(path+infile) as f:
        content = f.readlines()
        for lines in content:
            if "qber" in lines:
                data_in_next_line = True
                continue
            if data_in_next_line == True:
                if "uint" in lines:
                    data_in_next_line = False
                    splitted_line = lines.split(" ")
                    value = int(splitted_line[9])
                    if value < 10000 and value > 0:
                        qbers_quelle.append(value/100.0)
                if "7192576" in lines:
                    print lines
                    
plt.plot(qbers_quelle)
plt.grid()
plt.show