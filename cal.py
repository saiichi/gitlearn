# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 17:42:47 2014

@author: cuiyi
"""

import scipy.sparse as ssp
import cPickle as cpk
import numpy as np
from numpy import log
import random
#import warning


def jsd(x,y):
    x = np.array(x)
    y = np.array(y)
    d1 = x*np.log2(2*x/(x+y))
    d2 = y*np.log2(2*y/(x+y))
    d1[np.isnan(d1)] = 0
    d2[np.isnan(d2)] = 0
    d = 0.5*np.sum(d1+d2)    
    return d


def jsdsimcol(m,w1,w2):
    v1 = m[:,w1]
    v2 = m[:,w2]
    v1 = v1.toarray()[:,0]
    v2 = v2.toarray()[:,0]
    x = np.logical_and(v1>0,v2>0)
    v1 = v1[x]*1.0
    v2 = v2[x]*1.0
    return log(2) + 0.5*np.sum(v1*log(v1/(v1+v2))+v2*log(v2/(v1+v2)))
    #return jsdsim(v1,v2)
    
    
def jsdsimrow(m,w1,w2):
    v1 = m[w1,:]
    v2 = m[w2,:]
    v1 = v1.toarray()[0,:]
    v2 = v2.toarray()[0,:]
    x = np.logical_and(v1>0,v2>0)
    v1 = np.float(v1[x])
    v2 = np.float(v2[x])
    return log(2) + 0.5*np.sum(v1*log(v1/(v1+v2))+v2*log(v2/(v1+v2)))
    #return jsdsim(v1,v2)

def jsdsim(v1,v2):
    x = np.logical_and(v1>0,v2>0)
    v1 = v1[x]*1.0
    v2 = v2[x]*1.0
    return log(2) + 0.5*np.sum(v1*log(v1/(v1+v2))+v2*log(v2/(v1+v2)))    
    
def randCent(m,k):
    n = np.shape(m)[1]
    centroids = np.mat(np.zeros((k,n)))
    for j in range(n):
        v = m[:,j]
        minJ = np.min(v)
        rangeJ = np.max(v)-minJ
        centroids[:,j] = minJ + rangeJ*np.random.rand(k,1)
    return centroids

def Kmeans(dataset,k,distMeans=jsdsim,createCent=randCent):
    m = np.shape(dataset)[0]
    clusterAssment = np.mat(np.zeros((m,2)))
    centroids = createCent(dataset,k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):
            minDist = np.inf ; minIndex = -1
            for j in range(k):
                distJI = distMeans(np.array(centroids[j,:]),dataset[i,:])
                if distJI < minDist:
                    minDist = distJI; minIndex = j
            if clusterAssment[i,0] != minIndex:
                clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist
        print centroids
        for cent in range(k):
            ptsInclust = dataset[np.nonzero(clusterAssment[:,0].A==cent)[0]]
            centroids[cent,:] = np.mean(ptsInclust,axis=0)
    return centroids,clusterAssment
    
    

    




            

      