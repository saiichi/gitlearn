# -*- coding: utf-8 -*-
"""
Created on Wed May 21 19:07:20 2014

@author: Cuiyi
"""

from numpy import double
from numpy import array
import neurolab as nl
file = open("nndata.csv")

dataset=[]

for line in file.readlines():
     ll = line.strip().split(',')
     print ll
     if len(ll) == 2 and ll[0] != '' and ll[1]!='':
         dataset.append((double(ll[1]),double(ll[0])))
         
input = [z[0] for z in dataset]
output = [z[1] for z in dataset]

train = array(input).reshape(-1,1)
target = array(output).reshape(-1,1)
target = target/4.0

nn0 = nl.net.newff([[-1.5,1.5]],[1,1500,1])
nn1 = nl.net.newff([[-1.5,1.5]],[1,2000,1])
nn2 = nl.net.newff([[-1.5,1.5]],[1,2500,1])
err0 = nn0.train(train,target)
err1 = nn1.train(train,target)
err2 = nn2.train(train,target)

pred =  array(input).reshape(-1,1)
res0 = nn0.sim(pred)
res1 = nn1.sim(pred)
res2 = nn2.sim(pred)

x = array(range(len(input)))
yi = array(input)
yo1 = array(output)
yo2 = array(output)








