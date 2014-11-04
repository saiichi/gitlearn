# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 09:06:03 2014

@author: cuiyi
"""

from nltk.corpus import wordnet as wn
from cPickle import dump,load
from datasetread import multiProcessesCal2
from scipy.io import loadmat
from numpy.random import randint
import numpy as np
import cal2
from pprint import pprint

alllemmas=set()
f = open("workdata/wordnetalllemmadata.dat")
alllemmas = load(f)
f.close()

def getsynsetsnames(word):
    if type(word) != type(''):
        word = str(word)
    nset = set()
    for ss in wn.synsets(wn.morphy(word)):
        nset.add(ss.name.split('.')[0])
    return nset

def getlemmanames(word):
    if type(word) != type(''):
        word = str(word)
    nset = set()
    for ss in wn.synsets(wn.morphy(word)):
        nset.update(ss.lemma_names)
    return nset 
    
def getdefinitions(word):
    if type(word) != type(''):
        word = str(word)
    nlist = list()
    for ss in wn.synsets(wn.morphy(word)):
       nlist.append((ss.name.split('.')[1],ss.definition))
    return nlist

def getAlllemmas():
    lemmasets=set()
    for synset in list(wn.all_synsets()):
        lemmasets.update(synset.lemma_names)
    file = open("workdata/wordnetalllemmadata.dat",'w+')
    dump(lemmasets,file)

def shatter(tagset):
    global alllemmas
    tagset = set(tagset)
    ins = alllemmas.intersection(tagset)
    df = tagset.difference(alllemmas)
    newset = set()
    for e in df:
        m = wn.morphy(e)
        if m!=None:
            newset.add(e)
    ins2 = alllemmas.intersection(newset)
    return 1.0*(len(ins)+len(ins2))/len(tagset)

        
def calshatter(filelist):
    result={}
    for fname in filelist:
        r,t,u = multiProcessesCal2(fname,8)
        rate = shatter(t.keys())
        result.setdefault(fname,rate)
        print "%s has been cal, rate is %s" %(fname,str(rate)) 
    return result 

def jaccard(set1,set2):
    ins = set1.intersection(set2)
    return 1.0*len(ins)/len(set1)

    
def getweight(topsimset):
     weight = np.array([x[1] for x in topsimset])
     weight = np.e**(-weight)
     weight = weight-0.5
     weight = weight*(1/np.sum(weight))
     return weight

def morphy(topsimset):
    weight = np.array([x[1] for x in topsimset])
    weight = np.e**(-weight)
    weight = weight-0.5
    weight = weight*(1/np.sum(weight))
    topsimdict={}
    for i in range(len(topsimset)):
        k,v = topsimset[i]
        k = k.strip()
        if wn.morphy(k) != None:
            k = wn.morphy(k)
        topsimset[i]=(k,v)
        topsimdict.setdefault(k,weight[i])
    return topsimdict
        

def confirmSynset(tag,topsimset):
    topsimdict = morphy(topsimset)
    toptags = topsimdict.keys()
    decisionlist=[]
    for synset in wn.synsets(tag):
        decisionvalue = 0.0
        for lemma in synset.lemma_names:
            if lemma in toptags:
                decisionvalue += topsimdict[lemma]
        decisionvalue = decisionvalue/len(synset.lemma_names)
        decisionlist.append((synset,decisionvalue))
    decisionlist =  sorted(decisionlist,key = lambda z:z[1],reverse=True)
    return decisionlist[0][0],'self',decisionlist[0][1]
    
            
        
    
#def positionByLemma(tag,topsimset):
#    topsimdict = morphy(topsimset)
#    toptags = [x[0] for x in topsimset]
#    ins = alllemmas.intersection(toptags)
#    synsets = set()
#    for ele in ins:
#        synsets.update(wn.synsets(ele))
#    decisionlist=[]
#    for synset in synsets:
#        decisionvalue = 0.0
#        for lemma in synset.lemma_names:
#            if lemma in toptags:
#                decisionvalue += topsimdict[lemma]
#        decisionvalue=decisionvalue/len(synset.lemma_names)
#        decisionlist.append((synset,decisionvalue))
#    return sorted(decisionlist,key = lambda z:z[1],reverse=True)    
    
def matchWordnet(tag,topsimset):
    if wn.morphy(tag.strip()) == None:
        return  positionByClosure(topsimset)
    else:
        return confirmSynset(tag,topsimset) 

def calweightjaccard(lemmaset,topsimdict):
    decisionvalue = 0.0
    for lemma in lemmaset:
        if lemma in topsimdict.keys():
            decisionvalue += topsimdict[lemma]
    decisionvalue = decisionvalue/len(lemmaset)
    return decisionvalue


def positionByClosure(topsimset,top=3):
    topsimdict = morphy(topsimset)
    toptags = topsimdict.keys()
    ins = alllemmas.intersection(toptags)
    decisionlist=[]
    synsets = set()
    for ele in ins:
        synsets.update(wn.synsets(ele))
    hype = lambda s:s.hypernyms()
    hypo = lambda s:s.hyponyms()
    mh = lambda s:s.member_holonyms()
    mm = lambda s:s.member_meronyms()
    ph = lambda s:s.part_holonyms()
    pm = lambda s:s.part_meronyms()
    relationlist=[(hype,'hypernyms'),(hypo,'hyponyms'),(mh,'member_holonyms'),\
                 (mm,'member_meronyms'),(ph,'part_holonyms'),(pm,'part_meronyms')]
    newset = set(synsets)
    for synset in synsets:
        for fun,s in relationlist:
            newset.update(fun(synset))
    for synset in newset:
        decisionlist.append((synset,calweightjaccard(synset.lemma_names,topsimdict)))
    decisionlist = sorted(decisionlist,key=lambda x:x[1],reverse=True)
    #print decisionlist
    decision=[]
    for i in range(min([top,len(decisionlist)])):
        decision.append((decisionlist[i][0],'self',decisionlist[i][1]))
    result=[]
    for synset,s,weight in decision:
        decisionlist=[(synset,s,weight),]
        for fun,s in relationlist:
            for sn in fun(synset):
                decisionlist.append((sn,s,calweightjaccard(sn.lemma_names,topsimdict)))
        result.append(sorted(decisionlist,key=lambda x:x[2],reverse = True)[0])
    return result
    
    
def main():
    mdict = loadmat('workdata/dataset')
    m2 = mdict['mat2ed']
    taglist = mdict['taglist']
    rlist=[]
    randlist = randint(len(taglist),size=100)
    #f = open("workdata/wn22.dat",'w+')
    for i in randlist:
        topsimset = cal2.getTopSimilars(m2,taglist,i,20)
        rlist.append((taglist[i].strip(),matchWordnet(taglist[i].strip(),topsimset)))
        #f.write(str((taglist[i].strip(),matchWordnet(taglist[i].strip(),topsimset))))
    f = open('workdata/result.txt','w')
    f.write(str(pprint(rlist)))
    f.close()
    #dump(rlist,f)
    #f.close()
     
    

            
        

if __name__ == '__main__':
    main()
     

#x = getsynsetsnames(u'saddamhussein')
#print x
#getAlllemmas()        