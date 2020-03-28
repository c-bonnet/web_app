# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 11:41:50 2020

@author: Chae Gordon

could break it down it more but think it makes more sense to have each method
self consistent
"""

def cash(gross_revenue, cost_of_sales, da, tax_percent):
    ebitda = gross_revenue + cost_of_sales
    ebit = ebitda + da
    tax = -1*tax_percent*ebit
    cash = ebitda + tax
    return cash