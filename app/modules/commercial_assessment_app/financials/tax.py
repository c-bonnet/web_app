# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 11:48:55 2020

@author: Chae Gordon
"""

def tax(gross_revenue, cost_of_sales, da, tax_percent):
    ebitda = gross_revenue + cost_of_sales
    ebit = ebitda + da
    tax = -1*tax_percent*ebit
    return tax