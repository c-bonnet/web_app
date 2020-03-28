# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 15:45:51 2020

@author: Chae Gordon
"""

"""We want these as variable inputs for the app"""

#file name

file_name = "Gigha_data_half_hourly.xlsx"


# Inputs
site_type = "Wind"
site_capacity = 2000  # kW
export_capacity = 2000 #kW
import_capacity = 50  # kW

curtailed_price = 0.02  # £/kWh
grid_price = 0.15 # £/kWh
generator_price = 0.05 # £/kWh
spill_due_to_1_min = 0.14
agg_spill = 0.23

# opex inputs

data_cost = 960  # £/year
maintenance_cost = 822  # £/year
security_cost = 5000  # £/year
monitoring_cost = 3333  # £/year
