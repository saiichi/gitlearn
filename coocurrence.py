# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 18:56:34 2014

@author: cuiyi
"""

import numpy as np
import scipy.sparse as ssp
from numpy.core.fromnumeric import repeat


#import datasetread

def getCoocurrenceTag(filename):
    file = open(filename)
    text = file.readlines()
    flag = False
    uudict={} ; taglist=[]
    for line in text:
        ll = line.strip().split('\t')
        if len(ll) > 3:
            
            uu = (ll[1],ll[2])
            tag = ll[3]
            taglist.append(tag)
            if uudict.has_key(uu):
                flag = True
                uudict[uu].append(tag)
            else:
                uudict.setdefault(uu,[tag,])
    tagdict = {}
    taglist = list(set(taglist))
    for i in range(len(taglist)):
        tagdict.setdefault(taglist[i],i)
    r = []
    c = []
    if flag == True:
        for k,v in uudict.iteritems():
            for i in range(len(v)):
                for j in range(i+1,len(v)):
                    r.append(tagdict[v[i]])
                    c.append(tagdict[v[j]])
    
    mat = ssp.coo_matrix((repeat(1,len(r)),(r,c)),dtype=np.float64)                
    return flag,mat,tagdict
    
flag,mat,tagdict = getCoocurrenceTag("200410")
    
                
        
        