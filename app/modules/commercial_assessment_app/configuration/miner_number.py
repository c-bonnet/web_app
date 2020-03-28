# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 13:03:16 2020

@author: Chae Gordon
"""
from scipy.optimize import minimize
from powerbox_model import powerbox_model
import numpy as np

# if we already have a powerbox model which turns power into £
# then this is just finding the optimum number for this model
# maybe want this with interpolated data

# 2 year deployment is assumed

# powerbox model should output [Gross Revenue, C.O.S] C.O.S shoule be -ve!

def miner_number(power_series, miner_power_draw, miner_hashing_power, 
                 miner_cost, box_cost):
    
    def func(number):
        # variables for the power_box model
        variables = [power_series, miner_power_draw, miner_hashing_power]
        
        # turn power into revenue and cost of sales
        
        revenue_series = powerbox_model(number, variables)[0]  # revenue
        cos_series = powerbox_model(number, variables)[1]  # C.O.S
        
        # the financial outputs, dont actually need to annualise as roi isn't
        
        ebitda = sum(revenue_series) + sum(cos_series)
        capex = number*miner_cost + box_cost
        depreciation_amort = -1*(box_cost*(1/10) + 0.5*number*miner_cost)
        ebit = ebitda + depreciation_amort
        tax = -0.19*ebit
        net_profit = ebitda + tax
        
        # the return on investment
        roi = ((net_profit)/capex)
        
        return -1*roi
    
    # want to find the number that minimises -veROI
    initial_guess = int(np.average(power_series)/miner_power_draw)
    best_number = 0
    a = minimize(func, initial_guess, method='Nelder-Mead')
    best_number = a.x
    
    # PDU limit of miners
    if best_number > (9*48):
        best_number = 9*48
    # want box to be maximum 1MW
    if best_number*miner_power_draw > 1000:
        best_number = int(1000/miner_power_draw)
    return best_number
