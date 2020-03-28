# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 11:10:20 2020

@author: PeterParker
"""

"""
Residual Asset value calculator
Mark down: the fractional mark down on the asset at the end of a project
"""

# maybe want the inputs to be hardcoded or set once (earlier on for speed)
# Money in £
# time in years

capex_1 = 150000 
life_1 = 10
capex_2 = 0
life_2 = 2
deployment_length = 2

def residual_asset_value(mark_down):
    residual_1 = [capex_1*(1-(deployment_length/life_1)) if deployment_length/life_1 < 1 else 0][0]
    residual_2 = [capex_2*(1-(deployment_length/life_2)) if deployment_length/life_2 < 1 else 0][0]
    end_asset_value = (1-mark_down)*(residual_1 + residual_2)
    return end_asset_value
