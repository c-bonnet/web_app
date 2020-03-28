# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 15:27:02 2020

@author: Chae Gordon
"""
import math
import numpy as np
# Can't yet use np.array_split
# from numba import jit

# @jit(nopython=True, cache=True)
def monthly_agg(df, month=(48*365/12)):
    # df should be a np array if not --> np.asarray(df)
    split_m = np.array_split(np.asarray(df), math.ceil(len(df)/month)) 
    # split into months
    agg_months = np.zeros(len(split_m))
    for i in range(len(split_m)):
        agg_months[i] = np.sum(split_m[i])
    
    # agg_months = np.array([sum(i) for i in split_m]) 
    # aggregate the months
    
    return agg_months