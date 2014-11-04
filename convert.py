# -*- coding: utf-8 -*-
"""
Created on Thu Aug 07 13:00:32 2014

@author: Yi
"""
import numpy as np
from gensim import corpora

def csrtocorpus(row,col,val):
    nrow = np.max(row)
    p = 0
    corpus=[]
    for i in range(nrow):
        item = []
        l = len(row[row==i])
        for j in range(p,p+l):
            item.append((col[j],val[j]))
        corpus.append(item)
        p = p+l
    corpora.MmCorpus.serialize('workdata/corpus.mm',corpus)
    return corpus
    