# -*- coding: utf-8 -*-
"""
Created on Sun Jun  1 14:10:49 2014

@author: cuiyi
"""

import numpy as np
from numpy import random
from multiprocessing import Pool

from sklearn.cluster import KMeans
from cPickle import dump

#def datainput():
#    citynum = 9847
#    distmx = np.zeros((citynum,citynum))    
#    file = open("ja9847.txt")
#    dataset = np.zeros((9847,2))
#    i=0
#    for line in file.readlines():
#        ll = line.strip().split(' ')
#        dataset[i][0] = np.float(ll[1])
#        dataset[i][1] = np.float(ll[2])
#        i = i+1
#    for i in range(citynum):
#        for j in range(citynum):
#            dist = ((dataset[i]-dataset[j])**2).sum()
#            distmx[i,j] = np.sqrt(dist)
#    return dataset,distmx
    
def datainput(filename):
    #citynum = 9847
    #distmx = np.zeros((citynum,citynum))    
    file = open(filename)
    dataset = np.zeros((9847,2))
    i=0
    for line in file.readlines():
        ll = line.strip().split(' ')
        dataset[i][0] = np.float(ll[1])
        dataset[i][1] = np.float(ll[2])
        i = i+1
#    for i in range(citynum):
#        for j in range(citynum):
#            dist = ((dataset[i]-dataset[j])**2).sum()
#            distmx[i,j] = np.sqrt(dist)
    return dataset
    
def classifyfunc(dataset,n=100):
    labeler = KMeans(n_clusters=n)
    labeler.fit(np.mat(dataset))
    clusterdict = {}
    clusteridc = []
    for i in range(labeler.n_clusters):
        clusteridc.append([])
    for (row,label) in enumerate(labeler.labels_):
        clusterdict.setdefault(row,label)
        clusteridc[label].append(row)
    return clusterdict,clusteridc,labeler.cluster_centers_






def classifyfunc2(dataset):
    pass

            
            
        
            
            
        


def encode1(coderange,times = 200):
    length = len(coderange)
    code = np.array(coderange)
    for i in range(times):
        p1 = random.randint(length)
        p2 = random.randint(length)
        t = code[p1]
        code[p1] = code[p2]
        code[p2] = t
    return code
def PMXcrossover(p1,p2,rate=0.33):
    '''use PMX crossover'''
    length = len(p1)
    crosspoint1 = np.int(length*rate)
    crosspoint2 = np.int(length*(1-rate))
    c1 = np.array(p1)
    c2 = np.array(p2)
    
        
    t = p1[crosspoint1:crosspoint2]
    c1[crosspoint1:crosspoint2] = c2[crosspoint1:crosspoint2]
    c2[crosspoint1:crosspoint2] = t
    
    for i in range(crosspoint1):
        for j in range(crosspoint1,crosspoint2):
            if c1[i] == c1[j]:
                c1[i] = c2[j]
            if c2[i] == c2[j]:
                c2[i] = c1[j]
    for i in range(crosspoint2,length):
        for j in range(crosspoint1,crosspoint2):
            if c1[i] == c1[j]:
                c1[i] = c2[j]
            if c2[i] == c2[j]:
                c2[i] = c1[j]
    return c1,c2

def mutation(p):
    p = np.array(p)
    length = len(p)
    p1 = random.randint(length)
    p2 = random.randint(length)
    t = p[p1]
    p[p1] = p[p2]
    p[p2] = t
    return p

def eval_func(p,distmx,endpoint = False):
    distsum = 0.0
    if endpoint == False:
        for i in range(len(p)-1):
            distsum = distsum + distmx[p[i],p[i+1]]
        distsum = distsum + distmx[0,i+1]
#            else:
#                distsum = distsum + distmx[p[i+1],p[i]]
    else:
        start,end = endpoint
        distsum = distsum + distmx[start,p[0]]
        for i in range(len(p)-1):
            distsum = distsum + distmx[p[i],p[i+1]]
        distsum = distsum + distmx[p[len(p)-1],end]
    return distsum
    
def evalpop(pop,distmx,endpoint = False):
    evallist = []
    bestindi = pop[0]
    min = eval_func(pop[0],distmx,endpoint = endpoint)
    evallist.append(min)
    for i in range(1,len(pop)):
        dist = eval_func(pop[i],distmx,endpoint = endpoint)
        evallist.append(dist)
        if min>dist:
            min = dist
            bestindi = pop[i]
    bestindi = np.array(bestindi)
    return evallist,bestindi


def evalajust(evallist,alpha=0.5):
    evallist = np.array(evallist)
    ajusteval = (evallist-evallist.min())/(evallist.max()-evallist.min())
    return (1-ajusteval)+alpha
    
def roulette(pop,evallist,popsize=50):
    evallist = evalajust(evallist)
    rate = 1.0/np.sum(evallist)
    rl=[]
    cur = 0.0
    for i in range(len(pop)):
        cur = cur+rate*evallist[i]
        rl.append(cur)
    newpop = []
    for i in range(popsize):
        #flag=False
        shot = random.ranf()
        for j in range(len(rl)):
           if  shot<=rl[j]:
               #flag = True
               break;
        newpop.append(pop[j])
    return newpop
            
def gacompute(distmx,coderange,encode = encode1,popsize=50,selector=roulette,
              crossover = PMXcrossover,mutation=mutation,evalfunc = evalpop,
              initgens = 5000,crossoverrate=0.8,mutationrate=0.2,
              extinctionrate=2.5,extinctiontimes=10,endpoint=False,grate = 0.9,mark=-1,genslimit = 50000):
    '''ga with extinction'''
    maxgens = initgens
    pop = [] #Population 
    records = [] # record every generation best eval
    bestindirec =[]
    min = 0.0 # best eval now
    for i in range(popsize): #init
        pop.append(encode(coderange))
    evallist,bestindi = evalfunc(pop,distmx,endpoint=endpoint) #get eval for each individual into a list
    curmin = np.min(evallist)
    records.append(curmin)
    min = curmin
    #bestindi = np.array(pop[evallist.index(min)])
    g = 0 # times of extinction
    mutationac=0.0 
    crossoverac = 0.0
    extinctioncount=maxgens #extinction countdown
    while(g<extinctiontimes):
        
        newpop = [] 
        newpop.extend(pop)
        
        #crossover
        crossoverac = crossoverac + crossoverrate*popsize
        if np.int(np.int(crossoverac)/2) > 0:
            if np.int(crossoverac)%2 == 0:
                crossoverac = crossoverac - np.int(crossoverac)
                cochoice = random.choice(popsize,np.int(crossoverac),replace=False)
            else:
                crossoverac = crossoverac - np.int(crossoverac) +1
                cochoice = random.choice(popsize,np.int(crossoverac)-1,replace=False)
            for i in np.arange(len(cochoice),step=2):
                p1 = pop[cochoice[i]]
                p2 = pop[cochoice[i+1]]
                c1,c2 = crossover(p1,p2)
                newpop.append(c1)
                newpop.append(c2)
            
        #mutation
        mutationac = mutationac + popsize*mutationrate 
        if np.int(mutationac) > 0 :
            mchoice = random.choice(popsize,np.int(mutationac),replace=False)
            mutationac = mutationac - np.int(mutationac)
            for i in range(len(mchoice)):
                c = mutation(pop[mchoice[i]])
                newpop.append(c)
        
        extinctioncount = extinctioncount - 1  #extinction countdown      
        evallist,bestindicur = evalfunc(newpop,distmx,endpoint = endpoint) 
        curmin = np.min(evallist)
        records.append(curmin)
        if min>curmin: #
            if mark == -1:
                print "new best individual and maxgen=%d,now count to %d,net bet dist %d" %(maxgens,extinctioncount,min)
            bestindi = bestindicur
            if (maxgens-extinctioncount)*2.5 > maxgens:
                maxgens = (maxgens-extinctioncount)*2.5
                extinctioncount = maxgens
            min = curmin
        
        #extinction
        if extinctioncount <= 0:
            print "extionction %d .  best individual %d mark %d" %(g,min,mark)
            if grate*maxgens < initgens:
                maxgens = initgens
            else:
                maxgens = grate*maxgens
                if genslimit != 0 and maxgens > genslimit:
                    maxgens = genslimit
            pop = []
            for i in range(popsize):
                pop.append(encode(coderange))
            extinctioncount = maxgens
            g = g+1
            bestindirec.append(bestindi)
            evallist,bestindi = evalfunc(pop,distmx,endpoint=endpoint) #get eval for each individual into a list
            curmin = np.min(evallist)
            records.append(curmin)
            min = curmin 
        else:
            pop = selector(newpop,evallist,popsize = popsize)
    t,mostbestindi = evalfunc(bestindirec,distmx)
    return records,bestindirec,mostbestindi
    
    
def getnearestpoint(ci1,ci2,distmx):
    min = np.inf
    besti1=-1;besti2=-1
    for i1 in ci1:
        for i2 in ci2:
            if min > distmx[i1,i2]:
                min = distmx[i1,i2]
                besti1 = i1
                besti2 = i2
    return besti1,besti2
                
def getdistmx(dataset):
    n = np.shape(dataset)[0]
    distmx = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            dist = ((dataset[i]-dataset[j])**2).sum()
            distmx[i,j] = np.sqrt(dist)
    return distmx

def multiprocessgacompute(input):
    distmx,coderange,endpoint,mark = input
    popsize = len(coderange)*2
    initgens = popsize*50
    return gacompute(distmx,coderange,popsize = popsize,initgens = initgens,endpoint = endpoint,mark=mark)
        
cr = []
cb = []


def execute(distmx,cendistmx,ci,cc):
    global cr,cb
    cenrecords,br,cenbestindi = gacompute(cendistmx,range(len(cc)),popsize = 200,initgens=10000,extinctiontimes=4,extinctionrate=1.5,grate=0.8)
    cr = cenrecords
    cb = cenbestindi
    start = np.zeros((len(cenbestindi),))
    end = np.zeros((len(cenbestindi),))
    for i in range(len(cenbestindi)-1):
        p1,p2 = getnearestpoint(cenbestindi[i],cenbestindi[i+1],distmx)
        end[i] = p1
        start[i+1] = p2
    p1,p2 = getnearestpoint(cenbestindi[i+1],cenbestindi[0],distmx)
    end[i+1] = p1
    start[0] = p2
    input = []
    for i in range(len(cc)):
        coderange = list(ci[i])
        coderange.remove(start[i])
        coderange.remove(end[i])
        input.append((distmx,coderange,(start[i],end[i]),i))
    p = Pool(8) 
    return input,p.map(multiprocessgacompute,input)

def getstartend(distmx,cenbestindi,ci):
    start = np.zeros((len(cenbestindi),),dtype = np.int32)
    end = np.zeros((len(cenbestindi),),dtype = np.int32)
    for i in range(len(cenbestindi)-1):
        p1,p2 = getnearestpoint(ci[cenbestindi[i]],ci[cenbestindi[i+1]],distmx)
        end[i] = p1
        start[i+1] = p2
    p1,p2 = getnearestpoint(ci[cenbestindi[i+1]],ci[cenbestindi[0]],distmx)
    end[i+1] = p1
    start[0] = p2
    return start,end        
        
def execute2(distmx,cendistmx,ci,cc):
    global cr,cb
    cenrecords,br,cenbestindi = gacompute(cendistmx,range(len(cc)),popsize = 200,initgens=10000,extinctiontimes=6,extinctionrate=2.5,grate=0.9,genslimit = 500000)
    cr = cenrecords
    cb = cenbestindi
    
if __name__=='main':
    file = open("jtdataset1.dat",'wb')
    dataset,distmx = datainput()
    cd,ci,cc = classifyfunc(dataset)
    cendistmx = getdistmx(cc)
    dump(dataset,file)
    #dump(distmx,file)
    dump(ci,file)
    dump(cc,file)
    #dump(cendistmx,file)
    file.close()
    execute2(distmx,cendistmx,ci,cc)   
    file = open("jtresult1.dat",'wb')
    dump(cr,file)
    dump(cb,file)
    file.close()
            
        
        
    
    
    
            
        

























