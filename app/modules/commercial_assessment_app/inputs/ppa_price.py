# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 15:47:57 2020

@author: Chae Gordon
"""
"""
Calculated Inputs:
Days where aux imported: calculated from the gen data --> goes in OPEX
load_factor: from gen data
want to check that diurnal d/n have similar yields
"""
# As MVP just have a single price for PPA

"""

# Input tabs

winter_off_peak_price = 0.04
winter_off_peak_days = 7
winter_off_peak_hours = 12

winter_peak_price = 0.05
winter_peak_days = 5
winter_peak_hours = 12

summer_off_peak_price = 0.04
summer_off_peak_days = 7
summer_off_peak_hours = 12

summer_peak_price = 0.05
summer_peak_days = 5
summer_peak_hours = 12

# calculate the split of production between summer and winter
# quite tricky if all different lengths of data
# want to aggregate into months then sum all winter months then sum all summer months
# take in time series and turn to this

# df is a time series of generation data as POWER in kW
# time period is the time step in minutes of the generation data
# seasonal split outputs how much (%) energy is produced during WINTER (Oct-March).
# ISSUE is how to know which month the first data point starts in? --> 
# will recieve it like this so don't clean at as much as was before

#  for this file could potentially just drop the NaN values but would this scale?
# may need some form of cleanin or a "start date input"
# going forward will need to pre-clean data so that it comes with column headers
# as first row



# assume british date system
def month(date):
    if len(date) == 10:
        a = int(date[3:5])
    else:
        raise Exception('date string length ("x") should be 10. The value of x was: {}'.format(len(date)))
    return a

# could apply this transform to each element in row
# then sum the rows based on the value in this column with is_in conditional!

def seasonal_split(df, time_period, date_column):
    return 

# seasonal average of ppa_price to find the of peak

def seasonal_ppa_price():
    return

def ppa_price():
    return
    
"""

