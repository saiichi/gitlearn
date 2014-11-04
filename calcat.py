# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 18:56:44 2014

@author: cuiyi
"""

from cPickle import dump

import japanTSP as jt

file = open("jtdataset1.dat",'wb')
dataset,distmx = jt.datainput()
cd,ci,cc = jt.classifyfunc(dataset)
cendistmx = jt.getdistmx(cc)
dump(dataset,file)
dump(distmx,file)
dump(ci,file)
dump(cc,file)
#dump(cendistmx,file)
file.close()
#jt.execute2(distmx,cendistmx,ci,cc)   
file = open("jtresult1.dat",'wb')
dump(jt.cr,file)
dump(jt.cb,file)
file.close()