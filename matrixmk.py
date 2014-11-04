# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 13:37:27 2014

@author: cuiyi
"""
import numpy as np
from numpy.core.fromnumeric import repeat
import scipy.sparse as ssp
import cPickle as cpk
import sys


def mk2edMatrix(m):
    rlen,clen = m.shape
    v = np.array(m.sum(axis=0))
    v = 1.0/v[0,:]
    for i in range(len(v)):
        if v[i] == np.inf:
            v[i] = 0
    d = ssp.spdiags(v,0,clen,clen)
    d = d.tocsc()
    mdivu = m*d
    print mdivu.sum(axis=0)
    
    mt = m.transpose()
    rlen,clen = mt.shape
    v = np.array(mt.sum(axis=0))
    v = 1.0/v[0,:]
    for i in range(len(v)):
        if v[i] == np.inf:
            v[i] = 0
    d = ssp.spdiags(v,0,clen,clen)
    d = d.tocsc()
    mdivt = mt*d
    print mdivt.sum(axis =0)
    
    m2 = mdivu * mdivt
    return m2
    

def mk1stMatrix(r):
    row = []
    col = []
    for rl in r:
        row.extend(rl[0])
        col.extend(rl[1])
    val = repeat(1,len(row))
    m = ssp.coo_matrix((val,(row,col)),dtype=np.int32)
    m = m.tocsc()
    return m

if __name__ == '__main__':            
    flist = sys.argv
    flist.remove(flist[0])
    for filename in flist:
        file = open(filename,'rb')
        r = cpk.load(file)
        m1 = mk1stMatrix(r)
        m2 = mk2edMatrix(m1)
        file.close()
        file = open(filename+"mx",'wb')
        cpk.dump(m1,file)
        cpk.dump(m2,file)
    