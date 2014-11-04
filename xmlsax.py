# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 11:13:53 2014

@author: Yi
"""

from xml.sax import parse, handler, SAXException
from cPickle import dump,load
from scipy.sparse import coo_matrix,lil_matrix
from numpy import int32
import time
import gv


urllist=set()


class PreprocessHandler(handler.ContentHandler):
    def __init__(self):
        self.in_url = False
        self.in_tags = False
        self.in_tag=False
        self.in_tag_name = False
        self.in_tag_count = False
        self.cururl=""
        self.curtagname=""
        self.curtags=[]
        self.curtagcount=0
    def startElement(self, name, attr):
        if name==u'url':
            self.in_url = True
        if name==u'tags':
            self.in_tags = True
        if name==u'tag' and self.in_tags==True:
            self.in_tag = True
        if name==u'name' and self.in_tag ==True:
            self.in_tag_name=True
        if name==u'count' and self.in_tag==True:
            self.in_tag_count=True
    def endElement(self,name):
        if name==u'url':
            self.in_url = False
        if name==u'tags':
            self.in_tags=False
            gv.urldict.setdefault(self.cururl,self.curtags)
            self.curtags = []
        if name==u'tag' :
            self.in_tag = False
            self.curtags.append((self.curtagname,self.curtagcount))
        if name==u'name':
            self.in_tag_name=False
        if name==u'count':
            self.in_tag_count=False
    def characters(self,content):
        if self.in_url ==True:
            self.cururl=content
            gv.count += 1
        if self.in_tag_name == True:
            gv.tagset.add(content)
            self.curtagname=content
        if self.in_tag_count==True:
            self.curtagcount=int(content)

def buildCountMatrix():
    matr=[]
    matc=[]
    matv=[]
    #对所有的tag编号
    taglist = list(gv.tagset)
    #lilmat = lil_matrix((len(gv.urldict),len(gv.tagset)),dtype=int32)
    tagdict={}
    urldictc={}
    for i in range(len(taglist)):
        tagdict.setdefault(taglist[i],i)
    rcount = 0
    for url in gv.urldict.keys():
        urldictc.setdefault(url,rcount)
        for tag,count in gv.urldict[url]:
            matr.append(rcount)
            matc.append(tagdict[tag])
            matv.append(count)
        rcount += 1
        if rcount%500 == 0:
            print rcount
            
            
    coomat = coo_matrix((matv,(matr,matc)),shape=(len(gv.urldict),len(gv.tagset)))
    return tagdict,urldictc,coomat

def buildCountMatrix2():
    taglist = list(gv.tagset)
    lilmat = lil_matrix((len(gv.urldict),len(gv.tagset)),dtype=int32)
    tagdict={}
    urldictc={}
    for i in range(len(taglist)):
        tagdict.setdefault(taglist[i],i)
    rcount = 0
    for url in gv.urldict.keys():
        urldictc.setdefault(url,rcount)
        for tag,count in gv.urldict[url]:
            lilmat[rcount,tagdict[tag]] = count
        rcount += 1
        print rcount
    return tagdict,urldictc,lilmat
    
        
    

parse('workdata\social-odp-2k9_annotations.xml', PreprocessHandler())
datadumps = open("workdata\url-tagdata",'w+')
dump(gv.urldict,datadumps)
dump(gv.tagset,datadumps)
datadumps.close()
#dataloads = open("workdata/url-tagdata")
#gv.urldict = load(dataloads)
#gv.tagset = load(dataloads)
#print "All data load"
#starttime = time.time()
#tagdict,urldictc,coomat = buildCountMatrix()
#endtime = time.time()
#print "building matrix cost %dms" %(endtime-starttime)
#
#dataloads.close()
#
#datadumps = open("workdata/coomatdata",'w+')
#dump(tagdict,datadumps)
#dump(urldictc,datadumps)
#dump(coomat,datadumps)

        