# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 09:58:33 2020

@author: Chae Gordon
"""
import pandas as pd
import numpy as np
from numba import jit

# numba not saying power = object ? not sure why?

# want an if statement which checks the p_to_e_conv and adjusts the method
# MVP takes half hourly data (in Gigha format only) and converts it

# can have an if statement setting p_to_e_conv depending on a data type input

def data_parser(file, p_to_e_conv):
    df_2 = p_to_e_conv*pd.read_excel(file).values
    
    # transform 48 30 min rows into a time series
    float_arr = np.vstack(df_2[:, 2:50]).astype(np.float)
    size = int(len(df_2)*48)
    power = loop_transform(float_arr, size)
    df = pd.DataFrame(data=power, columns=["Average Power/ kW"])    
    return df

"""
d = np.asarray(df_2) # may not even need this part
float_arr = np.vstack(d[:, 2:48]).astype(np.float)
"""

"""
    # power = [df_2[i,j+2] for i in range(len(df_2)) for j in range(48)]
    power = []
    for i in range(len(df_2)):
        for j in range(48):
            power.append(df_2[i,j+2])
"""

"""
    power = []
    for i in range(len(df_2)):
        for j in range(48):
            power.append(df_2[i,j+2])
"""


# size = int(len(df_2)*48)
# power = loop_transform(float_arr, size)

@jit(nopython=True, cache=True)
def loop_transform(df_2, size):
    power = np.zeros(size)
    for i in range(len(df_2)):
        for j in range(48):
            power[i*48+j] = df_2[i,j]
    return power
    