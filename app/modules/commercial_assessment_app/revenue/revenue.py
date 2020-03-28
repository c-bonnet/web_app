# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 11:34:46 2020

@author: Chae Gordon

Takes a list of energy to monetised and outputs a total revenue
"""

import numpy as np

def energy_revenue(revenue_energy, energy_price):
    revenue_per_unit_time = energy_price*np.array(revenue_energy)
    total_revenue = sum(revenue_per_unit_time)
    return total_revenue