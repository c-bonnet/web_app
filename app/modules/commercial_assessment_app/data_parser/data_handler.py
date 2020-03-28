# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 16:17:02 2020

@author: PeterParker
"""

import pandas as pd

#  for this file could potentially just drop the NaN values but would this scale?
# may need some form of cleanin or a "start date input"
# going forward will need to pre-clean data so that it comes with column headers
# as first row

df_2 = pd.read_excel("Gigha_data_half_hourly.xlsx")
start_date = df_2["Settl. Date"][0]


# assume british date system
# could split later using regex

def month(date):
    if len(date) == 10:
        a = int(date[3:5])
    else:
        raise Exception('date string length ("x") should be 10. The value of x was: {}'.format(len(date)))
    return a

start_date = int(start_date[3:5])  

# could apply this transform to each element in row
# then sum the rows based on the value in this column with is_in conditional!
