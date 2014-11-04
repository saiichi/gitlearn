# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 19:04:00 2014

@author: cuiyi
"""

from cPickle import dump
from cPickle import load
import sys
import japanTSP as jt

prams = sys.argv
catfile = prams[1]
catres = prams[2]
spoint = int(prams[3])
epoint = int(prams[4])

file = open(catfile)
dataset = load(file)
distmx = load(file)
ci = load(file)
cc = load(file)
cendistmx = load(file)

file = open(catres)
cr = load(file)
cb = load(file)
file.close()

file.close()
file = open("subga"+prams[3]+"to"+prams[4],'wb')

for i in range(spoint,epoint):
    start,end = jt.getstartend(distmx,cb,ci)
    coderange = ci[cb[i]]
    coderange.remove(start[i])
    if start[i] != end[i]:
        coderange.remove(end[i])
    r,brec,bi = jt.gacompute(distmx,coderange,popsize = len(coderange),
                             initgens= len(coderange)*50,extinctionrate=2.5,
                            endpoint=(start[i],end[i]),mark=i,extinctiontimes=5,genslimit=100000)
    dump(bi,file)

    