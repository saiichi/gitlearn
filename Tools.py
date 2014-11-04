# -*- coding: utf-8 -*-
"""
Created on Sun Aug 17 15:55:53 2014

@author: Yi
"""

def generateLdaDict(topiclist):
    newlist=[]
    tagdict={}
    tagweight={}
    for topic in topiclist:
        topic = topic.strip().split(u'+')
        item=[]
        for tag in topic:
            tag = tag.strip().split(u'*')
            if float(tag[0])>0:
                item.append((tag[1],float(tag[0])))
        newlist.append(item)
    for i in range(len(newlist)):
        for tag,w in newlist[i]:
            if not tag in tagdict:
                tagdict.setdefault(tag,i)
                tagweight.setdefault(tag,w)
            else:
                if w>tagweight[tag]:
                    tagdict[tag] = i
                    tagweight[tag] = w
    return newlist,tagdict