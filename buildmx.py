# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 13:24:23 2014

@author: cuiyi
"""

import numpy as np
import scipy.sparse as ssp
import matrixmk as mx
import sys
import cPickle as cpk

def getHeader(text):
    taglist=[];urllist=[];linelist=[]
    for line in text:
        ll = line.strip().split('\t')
        if len(ll) == 4:
            taglist.append(ll[3])
            urllist.append(ll[2])
            linelist.append(ll)
    taglist = list(set(taglist))
    urllist = list(set(urllist))
    tagdict={};urldict={}
    for i in range(len(taglist)):
        tagdict.setdefault(taglist[i],i)
    for i in range(len(urllist)):
        urldict.setdefault(urllist[i],i)
    return tagdict,urldict,linelist
    
def buildmx(tagdict,urldict,linelist):
    mat1r=[];mat1c=[]
    matcor=[];matcoc=[]
    usrurldict={}
    for line in linelist:
        tag = line[3];url = line[2];uu = line[1],line[2]
        if usrurldict.has_key(uu):
            usrurldict[uu].append(tag)
        else:
            usrurldict.setdefault(uu,[tag,])
        
        mat1r.append(tagdict[tag])
        mat1c.append(urldict[url])
    for k,v in usrurldict.iteritems():
        for i in range(len(v)):
            for j in range(i+1,len(v)):
                matcor.append(tagdict[v[i]])
                matcoc.append(tagdict[v[j]])
    
    val = np.repeat(1,len(mat1r)) 
    mat1 = ssp.coo_matrix((val,(mat1r,mat1c)),dtype=np.int32)
    mat2 = mx.mk2edMatrix(mat1)
    mat1 = mat1.tocsc()
    val = np.repeat(1,len(matcor))
    matco = ssp.coo_matrix((val,(matcor,matcoc)),shape=mat2.shape,dtype=np.int32)
    matco = matco.tocsc()
    return mat1,mat2,matco

flist = sys.argv
#flist.remove(flist[0])
flist.append("200410")
for file in flist:
    f = open(file)
    tagdict,urldict,linelist = getHeader(f.readlines())
    mat1,mat2,matco = buildmx(tagdict,urldict,linelist)
    f.close()
    
    f = open(file+"cp",'wb')
    cpk.dump(tagdict,f)
    cpk.dump(urldict,f)
    cpk.dump(mat1,f)
    cpk.dump(mat2,f)
    cpk.dump(matco,f)
    



    
                
                
    
        