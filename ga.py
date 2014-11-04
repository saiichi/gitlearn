# -*- coding: utf-8 -*-
"""
Created on Thu May 15 13:27:19 2014

@author: cuiyi
"""

file = open("garesult.csv")
lines = file.readlines()
result=[]
for line in lines:
    listl = line.strip().split(',')
    if len(listl)==3:
        result.append(listl)
    
print result[0]
for r in result:
    r[0] = double(r[0][3:])
    r[1] = double(r[1][3:])
    r[2] = double(r[2][6:])
    