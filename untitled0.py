# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 15:59:24 2014

@author: Yi
"""
import numpy as np

file = open("scoreList.txt")
lines = file.readlines()
usrlist=[]
itmlist=[]
for i in range(len(lines)):
    lines[i] = lines[i].strip().split(' ')
    usrlist.append(lines[i][0])
    itmlist.append(lines[i][1])
usrlist = list(set(usrlist))
itmlist = list(set(itmlist))
usrdict = {}
itmdict = {}
for i in range(len(usrlist)):
    usrdict.setdefault(usrlist[i],i)
for i in range(len(itmlist)):
    itmdict.setdefault(itmlist[i],i)
dataset = np.mat(np.zeros((len(usrdict),len(itmdict))))
for ll in lines:
    dataset[usrdict[ll[0]],itmdict[ll[1]]] = np.float(ll[2])
np.savetxt("datset.csv",dataset)

