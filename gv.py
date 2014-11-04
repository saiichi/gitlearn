# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 12:20:52 2014

@author: Yi
"""
from cPickle import dump
tagdenotedict={}
urldenotedict={}
tagset=set()
taglist=[]
urllist=[]
coomatr=[]
coomatc=[]
coomatv=[]
doccount=0
tagscount=0
pstatus=0
corpus=[]
row_corpus=[]

def addTag(tag,count):
    global tagscount
    if tag in tagset:
        coomatr.append(doccount)
        coomatc.append(tagdenotedict[tag])
        coomatv.append(count)
    else:
        tagdenotedict.setdefault(tag,len(tagset))
        tagset.add(tag)
        taglist.append(tag)
        coomatr.append(doccount)
        coomatc.append(tagdenotedict[tag])
        coomatv.append(count)
    tagscount += 1
    if pstatus>1:
        print "Tag %s tagged by %d users has been added in matrix" %(tag,count)    

def endDoc(url):
    global  doccount,tagscount
    if pstatus>0:
        print "Url %s and no. %d tags under the url has been added in matrix" \
        %(url,tagscount)
    urldenotedict.setdefault(url,doccount)
    urllist.append(url)
    doccount += 1
    tagscount = 0
    
def addintocorpus(tag,count):
    pass
    
def save():
    file = open("workdata/gvdata.dat",'wt')
    dump(urllist,file)
    dump(taglist,file)
    file.close()

