# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 11:29:28 2020

@author: Chae Gordon

Takes a list of opex_energy used and outputs the total cost
"""
import numpy as np

def energy_opex(opex_energy, energy_cost):
    cost_per_unit_time = -1*energy_cost*np.array(opex_energy)
    total_cost = sum(cost_per_unit_time)
    return total_cost
