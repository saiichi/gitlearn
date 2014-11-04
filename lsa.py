# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 12:11:45 2014

@author: cuiyi
"""

import numpy as np
import scipy.sparse as ssp

def TFIDF2(dataset):
    '''This fuction is for sparse matrix. The type of dataset should be 
    scipy.sparse.csc.csc_matrix or scipy.sparse.csc.csr_matrix'''
    WordPerDoc = dataset.sum(axis=0).A[0,:]
    DocsPerWord = dataset.sum(axis=1).A[:,0]
    rows,cols = dataset.shape
    wpdiag = ssp.spdiags(1.0/WordPerDoc,0,cols,cols).tocsc()
    dataset = dataset*wpdiag
    dpdiag = ssp.spdiags(np.log(np.float(cols)/DocsPerWord),0,rows,rows)
    dataset = (dataset.transpose()*dpdiag).transpose()
    return dataset

    
    
    
    
    