# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 12:12:48 2020

@author: Chae Gordon
"""
import numpy as np

rev = [155*10**3,155*10**3]
cos = [-98*10**3,-98*10**3]

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
        return c,a,b
    
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
    
commercial_assessment = financials(1.3*10**5, rev, cos,45*10**3, 0.19, 2)

results =  {"irr" : commercial_assessment.irr(), 
            "moic" : commercial_assessment.moic(), 
            "payback period" : commercial_assessment.payback_period(), 
            "cash" : commercial_assessment.cash(), "irr cash" : commercial_assessment.irr_cash()}