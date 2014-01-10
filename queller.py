# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 20:45:19 2014

@author: damian
"""

import os
 
path = '../quelle/'
listing = os.listdir(path)
for infile in listing:
    print "current file is: " + infile