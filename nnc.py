# -*- coding: utf-8 -*-
"""
Created on Wed May 28 18:25:54 2014

@author: cuiyi
"""

import numpy as np

def cale(v1,v2):
    ve = v2-v1
    error = 0.0
    for e in ve:
        error = error+ e**2
    return error