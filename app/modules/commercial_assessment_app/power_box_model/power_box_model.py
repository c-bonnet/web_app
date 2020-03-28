# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 14:53:46 2020

@author: Chae Gordon
"""
# as a starting point just convert energy to useable energy
# if we begin with HH data we must interpolate then we can assess the useability
# as a % then apply this to the un-interpolated number

# At a later date should add curtailment
# add network stuff & other realism?

import numpy as np
from .loop_util import loop_jit

# check gen_enery is a numpy array

class power_box_model:
    def __init__(self, energy, var, capacity, load, aux_load, resolution):
        self.energy = energy  # kWh, should have already been transformed to time series
        self.var = var  # fractional sigma
        self.capacity = capacity  # kW
        self.load = load/float(self.capacity)  # normalised
        self.aux_load = aux_load/float(self.capacity)  # normalised
        self.resolution = resolution  # mins timescale of input data
        
        # interpolate will create the useable energy energy series to go 
        # with imported energy power series
        # and generated energy power series
        # it should first interpolate, then apply powerbox model
        # then aggregate the useable energy so its at the same time period
        
        # imported energy that is imported to run HPC should be added to useable
        # and to imported, as its revenue will be from useable buts COS from 
        #imported
        
    def useable_energy(self, hour=60):
        # need to normalise and then un-normalise
        # hour is the number of interpolated units of time in an hour eg.
        # for 1 min interpolation hour = 60
        # need to account for interpolation when re-scaling this is done by
        # dividing gen_max by the resolution
        "This isn't general !"
        p_to_e = self.resolution/hour  # 1/2 for default and HH data
        gen_energy = self.energy/p_to_e  # kW
        gen_capacity = self.capacity # kW
        gen_max = float(max(gen_energy))
        
        # normalise
        gen_energy = (1/gen_max)*gen_energy
                            
        exported_energy, imported_energy, useable_energy  = loop_jit(gen_energy, self.resolution, self.var, self.aux_load, self.load, hour)
        
        # un-normalise, remembering these are lists
        # want all lists to be the same length
        #  len_before_scale = len(useable_energy)
        
        useable_energy = useable_energy*(gen_capacity)
        # 1/hour has accounted for time period 1 min
        gen_energy = gen_energy*(gen_capacity)*p_to_e
        # must also convert back to energy
        # others don't need p_to_E as this is accounted for 1/hour factor
        imported_energy = imported_energy*gen_capacity
        exported_energy = exported_energy*(gen_capacity)
        
        #  len_after_scale = len(useable_energy)
        #  change_after_scale = len_before_scale-len_after_scale
        #  print(change_after_scale == 0)  
        # length remains the same
        # load is normalised so need capacity
        # want to find 30-min util?
        print(np.average(useable_energy))
        load_energy = (self.load*gen_capacity)*(1/hour)*np.ones(len(useable_energy))
        print(np.average(load_energy))
        util = np.average(useable_energy/load_energy)  # could avg. but think sum is faster
        
        return useable_energy, imported_energy, gen_energy, exported_energy, util
    
    def utilisation(self, p_to_E):
        # deprecated because it recalls interpolation method!
        # load is normalised so need capacity
        # want to find 30-min util?
        useable_energy = np.array(self.useable_energy()[0])
        load_energy = (self.load*self.capacity)*p_to_E*np.ones(len(useable_energy))
        util = sum(useable_energy)/sum(load_energy)  # could avg. but think sum is faster
        return util
