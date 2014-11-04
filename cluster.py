# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 11:58:45 2014

@author: cuiyi
"""
# from numpy.random import random 
# from scipy.sparse import * 
from sklearn.cluster import KMeans,MiniBatchKMeans
from cPickle import load
from time import time  

# create a 30x1000 dense matrix random matrix. 
# D = random((30,1000)) 
# keep entries with value < 0.10 (10% of entries in matrix will be non-zero)
# X is a "full" matrix that is intrinsically sparse.
# X = D*(D<0.10) # note: element wise mult  

# convert D into a sparse matrix (type coo_matrix) 
# note: we can initialize any type of sparse matrix. 
#           There is no particular motivation behind using 
#            coo_matrix for this example. 
# S = coo_matrix(X)   

# labeler = KMeans()
# convert coo to csr format 
# note: Kmeans currently only works with CSR type sparse matrix 
# labeler.fit(S.tocsr())  

# print cluster assignments for each row 
# for (row, label) in enumerate(labeler.labels_):   
#     print "row %d has label %d"%(row, label)

file = open("200601binmx")
load(file)
matDate = load(file)
matDate = matDate.transpose().tocsr()
start = time()
#labeler = KMeans()
#labeler.fit(matDate)
end = time()
print (end-start)*1000
start = time()
labeler = MiniBatchKMeans()
labeler.fit(matDate)
end = time()
print (end-start)*1000


clusterdict = {}
clusterres = []
for i in range(labeler.n_clusters):
    clusterres.append([])
for (row,label) in enumerate(labeler.labels_):
    clusterdict.setdefault(row,label)
    clusterres[label].append(row)
    

    