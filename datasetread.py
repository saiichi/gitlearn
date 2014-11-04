#!/usr/bin/python
#filename datasetread.py

import sys
import numpy as np
import scipy.sparse as ssp
import thread
import time
import cPickle as cpk
from multiprocessing.dummy import Pool
ROW=[]
COL=[]

def dataay(filename):
    try:
        file = open(filename)
        rlines = file.readlines()
        #print "rlines lens = %s" %len(rlines)
        lines = []
        for line in rlines:
            line = line.strip().split('\t')
            if len(line) == 4:
                lines.append(line)
        taglist = [line[-1] for line in lines]
        urllist = [line[2] for line in lines]
        taglist = list(set(taglist))
        urllist = list(set(urllist))
#        tagdict={}
#        urldict={}
#        for i in range(0,len(taglist)):
#            tagdict.setdefault(taglist[i],i)
#        for i in range(0,len(urllist)):
#            urldict.setdefault(urllist[i],i)
            
        #print len(taglist)
        #print len(urllist)
        return lines,taglist,urllist      
    except IOError,e:
        print e
        
def dataay2(filename):
    try:
        file = open(filename)
        rlines = file.readlines()
        #print "rlines lens = %s" %len(rlines)
        lines = []
        for line in rlines:
            line = line.strip().split('\t')
            if len(line) == 4:
                lines.append(line)
        taglist = [line[-1] for line in lines]
        urllist = [line[2] for line in lines]
        taglist = list(set(taglist))
        urllist = list(set(urllist))
        tagdict={}
        urldict={}
        for i in range(0,len(taglist)):
            tagdict.setdefault(taglist[i],i)
        for i in range(0,len(urllist)):
            urldict.setdefault(urllist[i],i)
            
        #print len(taglist)
        #print len(urllist)
        return lines,tagdict,urldict     
    except IOError,e:
        print e

def gm(lines,taglist,urllist,rresult,cresult,lock):
    row =[]
    col =[]
    for line in lines:
        r = taglist.index(line[-1])
        c = urllist.index(line[2])
        row.append(r)
        col.append(c)
    lock.acquire()
    rresult.extend(row)
    cresult.extend(col)
    lock.release()

def multiThreadsCal():
    lines,taglist,urllist = dataay("200512")
    print "put all data into memory"
    se = np.linspace(0,len(lines),9,endpoint=True)
    se = se.astype(np.int32)
    print se
    lock = thread.allocate_lock()
    print lock
    row=[]
    col=[]
    for i in range(0,8):
        thread.start_new_thread(gm,(lines[se[i]:se[i+1]],taglist,urllist,row,col,lock))
        print "start thread %s" % (i,)
    return row,col

def getdata(dataset):
    start = time.time()
    lines,taglist,urllist = dataset
    row =[]
    col =[]
    for line in lines:
        r = taglist.index(line[-1])
        c = urllist.index(line[2])
        row.append(r)
        col.append(c)
    end = time.time()
    print (end-start)*1000
    return row,col
    
def getdata2(dataset):
    start = time.time()
    lines,tagdict,urldict = dataset
    row =[]
    col = []
    for line in lines:
        r = tagdict[line[-1]]
        c = urldict[line[2]]
        row.append(r)
        col.append(c)
    end = time.time()
    print (end-start)*1000
    return row,col
    
    
def multiProcessesCal(filename,piecenum):
    start = time.time()
    lines,taglist,urllist = dataay(filename)
    pool = Pool(8) #because of the num of CPU cores
    se = np.linspace(0,len(lines),piecenum+1,endpoint=True)
    se = se.astype(np.int32)
    mapway = []
    for i in range(0,piecenum):
        mapway.append((lines[se[i]:se[i+1]],taglist,urllist))
    result=pool.map(getdata,mapway)
    end = time.time()
    print (end-start)*1000
    return result
    
    
def multiProcessesCal2(filename,piecenum):
    start = time.time()
    lines,taglist,urllist = dataay2(filename)
    pool = Pool(8) #because of the num of CPU cores
    se = np.linspace(0,len(lines),piecenum+1,endpoint=True)
    se = se.astype(np.int32)
    mapway = []
    for i in range(0,piecenum):
        mapway.append((lines[se[i]:se[i+1]],taglist,urllist))
    result=pool.map(getdata2,mapway)
    end = time.time()
    print (end-start)*1000
    return result,taglist,urllist
    
    
def getfilterdata(filename,k):
    lines,taglist,urllist = dataay(filename)
    tagcount={}
    urlcount={}
    start = time.time()
    for i in range(0,len(taglist)):
        tagcount.setdefault(taglist[i],0)
    for i in range(0,len(urllist)):
        urlcount.setdefault(urllist[i],0)

    for line in lines:
        tagcount[line[-1]] = tagcount[line[-1]] + 1
        urlcount[line[2]] = urlcount[line[2]] + 1
    end = time.time()
    print (start-end)*1000
    tagdict = {}
    urldict = {}
    nt=0; nc=0 
    start = time.time()
    for tag in taglist:
        if tagcount[tag] >= k:
            tagdict.setdefault(tag,nt)
            nt = nt +1
    for url in urllist:
        if urlcount[url] >=k:
            urldict.setdefault(url,nc)
            nc = nc +1
    end = time.time()
    print (start-end)*1000
    print len(tagdict)
    print len(urldict)
    row =[]
    col = []
    start = time.time()
    tk = tagdict.keys()
    uk = urldict.keys()
    for line in lines:
        tag = line[-1]
        url = line[2]
        if tag in tk and url in uk:
            row.append(tagdict[tag])
            col.append(urldict[url])
    end = time.time()
    print (start-end)*1000
    fw = open(filename+"binf"+str(k),'wb')
    result = [(row,col)]
    cpk.dump(result,fw)
    cpk.dump(tagdict,fw)
    cpk.dump(urldict,fw)
    
def plusFile(sf,pfl):
    file = open(sf)
    r = cpk.load(file)
    st = cpk.load(file)
    stsize = len(st)
    #stk = st.keys()
    su = cpk.load(file)
    susize = len(su)
    #suk = su.keys()
    file.close()
    #print len(srow),len(scol)
    print len(st),len(su)
    srow=[]
    scol=[]
    for re in r:
        srow.extend(re[0])
        scol.extend(re[1])
    for fn in pfl:
        file = open(fn)
        r = cpk.load(file)
        pt = cpk.load(file)
        pu = cpk.load(file)
        file.close()
        prow=[]
        pcol=[]
        for re in r:
            prow.extend(re[0])
            pcol.extend(re[1])
            
        cdt = {}
        for ptag,pv in pt.iteritems():
            if ptag in st.keys():
                cdt.setdefault(pv,st[ptag])
            else:
                st.setdefault(ptag,stsize)
                cdt.setdefault(pv,stsize)
                stsize= stsize+1
        for i in range(len(prow)):
            prow[i] = cdt[prow[i]]
        srow.extend(prow)
        
        cdu={}
        for purl,pv in pu.iteritems():
            if purl in su.keys():
                cdu.setdefault(pv,su[purl])
            else:
                su.setdefault(pv,susize)
                cdu.setdefault(pv,susize)
                susize = susize+1
        for i in range(len(pcol)):
            pcol[i] = cdu[pcol[i]]
        scol.extend(pcol)
    filename = sf+"plus"
    for pfn in pfl:
        filename+=pfn
    file = open(filename,'wb')
    cpk.dump((srow,scol),file)
    cpk.dump(st,file)
    cpk.dump(su,file)
                
                
            
        

#flist = sys.argv
#flist.remove(flist[0])
#print flist
#for filename in flist:
#    #filename="200404"    
#    r,t,u = multiProcessesCal2(filename,8)
#    file = open(filename+"bin",'wb')
#    cpk.dump(r,file)
#    cpk.dump(t,file)
#    cpk.dump(u,file)   
#plusFile("200401bin",["200310bin"])
paramlist = sys.argv
paramlist.remove(paramlist[0])
# paramlist.append("200501")

#for param in paramlist:
#    flist = param.split("+")
#    if len(flist) > 1:
#        plusFile(flist[0],flist[1:])
#    else:
#        fn = flist[0]
#        r,t,u = multiProcessesCal2(fn,8)
#        file = open(fn+"bin",'wb')
#        cpk.dump(r,file)
#        cpk.dump(t,file)
#        cpk.dump(u,file)

  
    
    
    

    
    
