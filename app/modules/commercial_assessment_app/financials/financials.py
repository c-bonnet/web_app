# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 13:03:23 2020

@author: PeterParker
"""
import numpy as np
# from numba import jit

"""
Want exception raising
"""

class financials:
    def __init__ (self, capex, gross_revenue, cost_of_sales, da, tax_percent
                  , years):
        self.capex = [-1*capex]
        self.gross_revenue = np.array(gross_revenue)
        self.cost_of_sales = np.array(cost_of_sales)
        self.da = -da*np.ones(len(gross_revenue))
        self.tax_percent = tax_percent
        self.years = years
    
    def asset_disposal(self):
        residual_value = -1*self.capex[0] + self.years*self.da[0]
        return residual_value
    
    def ebitda(self):
        ebitda = self.gross_revenue + self.cost_of_sales
        return ebitda
    
    def ebit(self):
        ebitda = self.ebitda()
        ebit = ebitda + self.da
        return ebit
    
    def tax(self):
        ebit = self.ebit()
        tax = -1*self.tax_percent*ebit
        return tax
    
    def cash(self):
        cash = self.ebitda() + self.tax()
        return cash
    
    def irr_cash(self):
        a = np.array(self.capex)
        b = self.cash()
        b[-1] += self.asset_disposal() 
        c = np.concatenate((a, b), axis=None)
        return c
    
    def irr(self):
        a = np.array(self.capex)
        b = self.cash()
        b[-1] += self.asset_disposal() 
        c = np.concatenate((a, b), axis=None)
        irr_result = np.irr(c)
        return irr_result
    
    def moic(self):
        moic = float(sum(self.cash())+self.asset_disposal())/float(-1*self.capex[0])
        return moic
    
    def payback_period(self):
        pb_period = -1*self.capex[0]/np.average(self.cash())
        return pb_period


"""
irr_result = irr_calc(self.capex, self.cash(), self.asset_disposal())
@jit(nopython=True, cache = True)
def irr_calc(capex, cash, asset_disposal):
        a = np.array(capex)
        b = cash
        b[-1] += asset_disposal
        c = np.concatenate((a, b), axis=None)
        irr_result = np.irr(c)
        return irr_result
"""