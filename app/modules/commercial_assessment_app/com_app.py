# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 15:29:07 2020

@author: Chae Gordon
"""
import numpy as np
from data_parser import to_time_series
from inputs import inputs
from power_box_model import power_box_model
from revenue_assumptions import pound_per_kwh
from opex import ex_energy_opex
from revenue import monthly_aggregator
from financials import financials

"""The Commercial assessment Model"""

month_1_min = 30*48*365/12
month_hh = 48*365/12

# inputs from a json config file (can be re-written by the form submission)
capacity = 2000 # inputs.export_capacity
# need this uplifted in future
gen_energy_cost = inputs.generator_price  
# want this coming from json in future
imort_energy_cost = inputs.grid_price
# annual ex-energy opex 
data_cost = inputs.data_cost
maintenance_cost = inputs.maintenance_cost
security_cost = inputs.security_cost
monitoring_cost = inputs.monitoring_cost
var = 0.02
pb_load = 133
aux_load = 7.4
resolution = 30
miner_power = 3.344
miner_terahash = 88
export_revenue_per_e = inputs.generator_price

############################################################ Step 1: Load data

# takes 5 years of Gigha data and turns it into a time series of HH data
# second parameter should scale to 30 minutes levels ie, 3 if 10 minutes
df = to_time_series.data_parser("Gigha_data_30_min.xlsx",1)  
# keeping as energy kWh
energy_values = df.values

############################### Step 2: Apply Powerbox model to the power data

model = power_box_model.power_box_model(energy_values, var, capacity, pb_load, aux_load, 
                                        resolution).useable_energy()

model_u = power_box_model.power_box_model(energy_values, var, capacity, pb_load, aux_load, 
                                        resolution).utilisation(1/60)

# once start adding imports due to power drive will require changing useable 
# interpolated to interpolated plus useable import
# outputs (useable_energy, imported_energy, generator_energy, exported_energy)
# generator energy is on same time scale as data source file

#################################################### Step 3: financial methods

#  i) getting revenue assumptions

pound_per_e = pound_per_kwh.pounds_per_kwh(miner_power, miner_terahash)  # £/kWh
export_revenue_per_e = inputs.generator_price

#  ii) opex assumptions

# energy_opex per kWh

annual_ex_energy_cost = ex_energy_opex.ex_energy_opex(data_cost, 
                                                      maintenance_cost, 
                                                      security_cost, 
                                                      monitoring_cost)

# outputs as a dictionary so can be manipulated easily in python

#  Aggregate energy values to months

monthly_useable_energy = monthly_aggregator.monthly_agg(model[0], month_1_min)
monthly_imported_energy = monthly_aggregator.monthly_agg(model[1], month_1_min)
monthly_generator_energy = monthly_aggregator.monthly_agg(model[2], month_hh)
monthly_exported_energy = monthly_aggregator.monthly_agg(model[3], month_1_min)

#  iv) gross revenue
# only take full years to account for seasonality
gross_revenue = 0.25*(pound_per_e*sum(monthly_useable_energy[:48]) + export_revenue_per_e*sum(monthly_exported_energy[:48]))*np.ones(2)

# v) gross cost of sales
gross_cos = (-0.25*(imort_energy_cost*sum(monthly_imported_energy[:48]) + gen_energy_cost*sum(monthly_generator_energy[:48]))-annual_ex_energy_cost)*np.ones(2)

commercial_assessment = financials.financials(2*10**5, gross_revenue, gross_cos, 
                                              45.2*10**3, 0.19, 2)

results_1 =  {"irr" : commercial_assessment.irr(), 
            "moic" : commercial_assessment.moic(), 
            "payback period" : commercial_assessment.payback_period(), 
            "cash" : commercial_assessment.cash()}