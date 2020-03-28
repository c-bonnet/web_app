# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 13:50:59 2020

@author: Chae Gordon

# try np.where and np.logical to vectorise loop
# refactor & make type inference better
# try parallel and prange (check it is applicable)
# parallel = True, need p range
"""

import numpy as np
from numba import jit
# import time
# import pandas as pd

"""This is the main function in the Powerbox model. It takes a set of energy 
generation and interpolates it to produce a power time series at a fine enough
grain to simulate Powerbox operation."""

# want types declared

"""
This function doesn't explicitly change dimensions but the subfunctions do by multiplying by 1/hour
input = power | output = energy going foward I think this should be done only at the end
Inputs: 
    1) gen_power the generation time series. (np.array) shape= , dim = kW  [SILLY variable name]
    2) resolution the resolution of gen_energy in minutes (float)
    3) var is the 1-min sigma of wind (float)
    4) aux_load the auxillary load in kW (float)
    5) load the IT load in kW (float)
    6) hour is the number of interpolated units in an hour, for 1-min = 60 (float)
    
Outputs:
    1) exported_energy is a time series of energy exported to the grid (np.array) dim = kWh
    2) imported_energy is a time-series of imported energy to supplement the
    Powerbox supply(np.array) dim = kWh
    3)useable_energy is a time series of the energy that is useable to the Powerbox
    we assume that this is equivalent to the amount that will be used but stil
    need to add a powerdrive model to get the actual used amount.(np.array) dim = kWh"""

@jit(nopython=True, cache=True) 
def loop_jit(gen_power, resolution, var, aux_load, load, hour):
    #inputs (np.array, float, float, 
    # gen_energy must now be a numpy array
    size = (len(gen_power)-1)*resolution
    interpolated = np.zeros(size)
    imported_energy = np.zeros(size)
    exported_energy = np.zeros(size)
    useable_energy = np.zeros(size)
    
    for i in range(len(gen_power)-1):
        for j in range(resolution):
            # have it so random fluctuation is centred on previous point
            a = interpolate_logic(gen_power[i], interpolated[i*resolution+j-1], var, j)
            interpolated[i*resolution+j] = a
            
            """ Replace previous big stack of logic with whole logic function"""
            
            # take values in and give values out
            imported_energy[i*resolution+j], exported_energy[i*resolution+j], useable_energy[i*resolution+j] = whole_logic(a, aux_load, load, hour)

    return exported_energy, imported_energy, useable_energy 

@jit(nopython=True, cache=True)
def interpolate_logic(gen_power_point, interpolated_point, var, j):
    # interpolated_point = interpolated[i+j-1]
    # gen_energy_point = gen_energy[i]
    if j > 0:
        a = interpolated_point + np.random.normal(loc=0,scale=var)
    else:
        a = gen_power_point + np.random.normal(loc=0,scale=var)
    return min(max(a,0),1)

@jit(nopython=True, cache=True)
# could also try return max(0,calculated)
def import_logic(a, aux_load, hour):
    # function same as :
    # imported_amount = [(aux_load - a)*(1/hour) if a < aux_load else float(0)][0]
    imported_amount = max((aux_load - a)*(1/hour), 0)
    return imported_amount

@jit(nopython=True, cache=True)
# could use max also with load in it already
def useable_logic(a, aux_load, hour):
    # function same as :
    # useable_amount = [(a - aux_load)*(1/hour) if import_logic(a,aux_load,hour) == 0 else float(0)][0]
    useable_amount = max((a - aux_load)*(1/hour),0.0)
    return useable_amount


@jit(nopython=True, cache=True)
def gen_rel_logic(load, aux_load, a, hour, useable_amount):
    useable_energy = min((load)*(1/hour),useable_amount)
    exported_energy = max(0,(a-load-aux_load)*(1/hour))
    """
    if a < load+aux_load:
        exported_energy = float(0)
        useable_energy = useable_amount
    else:
        exported_energy = (a-load-aux_load)*(1/hour)
        useable_energy = (load)*(1/hour)
    """
    return exported_energy, useable_energy

@jit(nopython=True, cache=True)
def whole_logic(a, aux_load, load, hour):
    "if a > 0:"
    imported_energy = import_logic(a,aux_load,hour)
    useable_amount = useable_logic(a,aux_load,hour)
    exported_energy, useable_energy = gen_rel_logic(load, aux_load, a, hour, useable_amount)
    """
    else:
        exported_energy = float(0)
        imported_energy = aux_load*(1/hour)
        useable_energy = float(0)
    """
    
    return (imported_energy, exported_energy, useable_energy)