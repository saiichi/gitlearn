# -*- coding: utf-8 -*-
"""
Created on Wed Aug 06 13:36:01 2014

@author: Yi
"""

import networkx as nx
from scipy.sparse import coo_matrix
from scipy.io import savemat

def build1stmatgraph(m1):
    m1 = m1.tocoo()
    #g= nx.Graph()
    nrow,ncol = m1.shape
    row = m1.row
    col = m1.col + nrow
    val = m1.data
    m = coo_matrix((val,(row,col)),shape=(nrow+ncol,nrow+ncol)).tocsc()
    savemat('workdata/Adj',mdict={'adj':m})
    return nx.from_scipy_sparse_matrix(m)
    
def deleteEdgesUnderWeight(g,weightlimit=10):
    edges = g.edges()
    for u,v in edges:
        if g.get_edge_data(u,v)['weight'] < weightlimit:
            g.remove_edge(u,v)
    

def getConnectComponentMap(g,taglist,offset=12616):
    componentlist=nx.connected_components(g)
    tagdict={}
    for i in range(len(componentlist)):
        component = componentlist[i]
        for j in range(len(component)):
            component[j] = taglist[component[j]-offset]
            tagdict.setdefault(component[j],i)
    return tagdict,componentlist
            
def basic_info(G):
    f=open('basic_info.txt','w')
    f.write('网络节点数：')
    f.write(str(G.number_of_nodes()) + '\n')
    f.write('网络边数：')
    f.write(str(G.size()) + '\n')
    f.write('网络边加权和：')
    f.write(str(G.size(weight='weight')) + '\n')
    scc=nx.strongly_connected_components(G)#返回强连通子图的list
    wcc=nx.weakly_connected_components(G)#返回弱连通子图的list
    f.write('弱连通子图个数：')
    f.write(str(len(wcc)) + '\n')
    f.write('强连通子图个数：')
    f.write(str(len(scc)) + '\n')
    largest_scc=scc[0]#返回最大的强连通子图
    f.write('最大强连通子图节点数：')
    f.write(str(len(largest_scc)) + '\n')
    f.write('有向图平均路径长度：')
    f.write(str(nx.average_shortest_path_length(G)) + '\n')
    G=G.to_undirected()
    f.write('平均聚类系数：')
    f.write(str(nx.average_clustering(G)) + '\n')
    f.write('平均路径长度：')
    f.write(str(nx.average_shortest_path_length(G)) + '\n')
            
    