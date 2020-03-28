# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 11:26:41 2020

@author: Chae Gordon
"""
from numba import jit

@jit(nopython=True, cache = True)
def ex_energy_opex(data_cost, maintenance_cost, security_cost, 
                   monitoring_cost):
    a = data_cost
    b = maintenance_cost
    c = security_cost
    d = monitoring_cost
    return a + b + c + d 

