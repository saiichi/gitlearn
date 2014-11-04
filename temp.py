# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 09:43:15 2014

@author: cuiyi
"""

import numpy as np


import japanTSP as jt
file = open("jaresult")
x = []
for t in file.readlines():
    x.append(int(t.strip())-1)
    

dataset = jt.datainput("ja9847.txt")
indicate = x
x = []
y =[]
indicate
for i in indicate:
    x.append(dataset[i][0])
    y.append(dataset[i][1])
x1 =x
y1 =y
indicate1 =  indicate   
    
for i in range(300):
    p = np.random.randint(9800)
    o = np.random.randint(5)
    
    t = x1[p]
    x1[p] = x1[p+o]
    x1[p+o] = t
    t = y1[p]
    y1[p] = y1[p+o]
    y1[p+o] = t
    t = indicate1[p]
    indicate1[p] = indicate1[p+o]
    indicate1[p+o] = t



         