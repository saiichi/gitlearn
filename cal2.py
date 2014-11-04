# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 15:51:01 2014

@author: cuiyi
"""

from cPickle import dump
from scipy.io import loadmat
import numpy as np
import sys
import cal
import time
#from wikiapi import WikiApi
import wordnet as wn2

def getRandTag(m,k,maxnum):
    row,col = np.shape(m)
    rtl = np.random.randint(0,col,size=k)
    result = []
    for i in rtl:
        r=[]
        v1 = m[:,i].toarray()
        for j in range(col):
            r.append((j,cal.jsdsim(v1,m[:,j].toarray())))
        r = sorted(r,key = lambda x:x[1])
        result.append(r[0:maxnum])
    return rtl,result
        
def getTopSimilars(m2,rtd,w,top):
    row,col = m2.shape
    result = []
    for i in range(col):
        result.append((rtd[i],cal.jsdsimcol(m2,w,i)))
    result = sorted(result,key = lambda x:x[1])
    if top>0:
        return result[:top]
    else:
        return result

def main():
    mdict = loadmat("workdata/cscmat")
    mdict2 = loadmat("workdata/m2",)
    taglist = mdict['taglist']
    m2 = mdict2['m2mat']
    tagdict = {}
    alltnum = len(taglist)
    for i in range(len(taglist)):
        tagdict.setdefault(taglist[i],i)
    rdict={}
    f = open("workdata/topresult.dat",'wt')
    i=0
    for tag in tagdict.keys():
        i+=1
        rdict.setdefault(tag,getTopSimilars(m2,taglist,tagdict[tag],20))
        #f.write(tag+'|'+str(getTopSimilars(m2,taglist,tagdict[tag],20))+'\n')
        #print "complete percent:" + str(100.0*i/alltnum)+"%\r" 
        sys.stdout.write("complete percent:" + str(100.0*i/alltnum)+"%\r" )
        dump(rdict,f)
        
    
    #dump(rdict,f)
    f.close()

    
               
    
if __name__ == '__main__':
    main()
        
                

#flist =  sys.argv
#flist.remove(flist[0])
#print flist
#flist.append("200309")
#
#for filename in flist:
#    
#    start = time.time()
#    file = open(filename+"bin")
#    cpk.load(file)
#    tagdict = cpk.load(file)
#
#    urldict = cpk.load(file)
#    file.close()
#    
#    file = open(filename+"binmx")
#    m1 = cpk.load(file)
#    m2 = cpk.load(file)
#    file.close()
#    end = time.time()
#    print u'Loading data cost %d'    %((end-start)*1000,)
#    rtl,result = getRandTag(m2,8,10)
#    
###    print rtl
###    print result
#    rtd = {};rud = {}
#    for k,v in tagdict.iteritems():
#        rtd.setdefault(v,k)
#    for k,v in urldict.iteritems():
#        rud.setdefault(v,k)
#        
#    print getTopSimilars(m2,rtd,25,10)
#    result = []
#    for word in rtl:
#        print rtd[word]
#        result.append((word,getTopSimilars(m2,rtd,word,10),
#                       wn2.getsynsetsnames(rtd[word]),
#                       wn2.getlemmanames(rtd[word]),
#                       wn2.getdefinitions(rtd[word]) ))
#    print result
        
        
        
#    #rtl = list(rtl)
#    ar = {}
#    for i in range(len(rtl)):
#        #rtl[i] = rtd[rtl[i]]
#        ar.setdefault(rtd[rtl[i]],[])
#        r = result[i]
#        for j in range(len(r)):
#            k,v = r[j]
#            r[j] = rtd[k],v
#        ar[rtd[rtl[i]]].extend(r)
#    file = open("binout"+filename,'wb')
#    cpk.dump(ar,file)
#    file.close()
#    end = time.time()
#    print (end-start)*1000
#    print ar
#    w = WikiApi()
#    wr = {}
#    for keyw in ar.keys():
#        try:
#            w.execute(unicode(keyw))
#        except:
#            w.missing = True
#        if w.missing == True:
#            wr.setdefault(keyw,"missing")
#        else:
#            tags = [str(e[u'title']).lower() for e in w.links]
#            kt = tagdict.keys()
#            r = []
#            for tag in tags:
#                if not tag in kt:
#                    r.append((tag,np.log(2)))
#                else:
#                    r.append((tag,cal.jsdsimcol(m2,tagdict[keyw],tagdict[tag])))
#            r = sorted(r,key = lambda x:x[1])
#            wr.setdefault(keyw,r)
#    print wr
            
        
            
                
                
            
            
    
    
    
        
    
    
    