import numpy as np
from .data_parser import to_time_series
from .power_box_model import power_box_model
from .revenue_assumptions import pound_per_kwh
from .opex import ex_energy_opex
from .revenue import monthly_aggregator
from .financials import financials
import time

"""This has file name hardcoded"""

class CommercialApp:
    def __init__(self, inputs_dict):
        for k,v in inputs_dict.items():
            setattr(self, k, v)
            
    def get_data(self):
        # takes 5 years of Gigha data and turns it into a time series of HH data
        # second parameter should scale to 30 minutes levels ie, 3 if 10 minutes
        df = to_time_series.data_parser(self.file, self.hh_factor)  
        # keeping as energy kWh
        energy_values = df.values.ravel()  # flattens data into array not array of lists
        return energy_values
    
    def powerbox_model(self):
        start = time.time()
        energy_values = self.get_data()
        end = time.time()
        print("Elapsed get data = %s" % (end - start))
        # start = time.time()
        model_object = power_box_model.power_box_model(energy_values, self.var, self.capacity, self.pb_load, self.aux_load, self.resolution)
        # end = time.time()
        # print("Elapsed instantiate = %s" % (end - start))
        start = time.time()
        model = model_object.useable_energy()
        end = time.time()
        print("Elapsed interpolate = %s" % (end - start))
        # start = time.time()
        model_u = model[4]
        # end = time.time()
        # print("Elapsed utilisation = %s" % (end - start))
        return model, model_u
    
    def run(self):
        start = time.time()
        #  i) getting revenue assumptions
        starty = time.time()
        pound_per_e = pound_per_kwh.pounds_per_kwh(self.miner_power, self.miner_terahash)  # £/kWh
        export_revenue_per_e = self.gen_energy_cost

        #  ii) opex assumptions

        # energy_opex per kWh

        annual_ex_energy_cost = ex_energy_opex.ex_energy_opex(self.data_cost, 
                                                              self.maintenance_cost, 
                                                              self.security_cost, 
                                                              self.monitoring_cost)

        # outputs as a dictionary so can be manipulated easily in python
        endy = time.time()
        print("Elapsed before powerbox model = %s" % (endy - starty))
        #  Aggregate energy values to months
        modely = self.powerbox_model()
        starty = time.time()
        monthly_useable_energy = monthly_aggregator.monthly_agg(modely[0][0], self.month_1_min)
        monthly_imported_energy = monthly_aggregator.monthly_agg(modely[0][1], self.month_1_min)
        monthly_generator_energy = monthly_aggregator.monthly_agg(modely[0][2], self.month_hh)
        monthly_exported_energy = monthly_aggregator.monthly_agg(modely[0][3], self.month_1_min)

        #  iv) gross revenue
        # only take full years to account for seasonality
        gross_revenue = 0.25*(pound_per_e*sum(monthly_useable_energy[:48]) + export_revenue_per_e*sum(monthly_exported_energy[:48]))*np.ones(2)

        # v) gross cost of sales
        gross_cos = -1*(0.25*(self.imort_energy_cost*sum(monthly_imported_energy[:48]) +self.gen_energy_cost*sum(monthly_generator_energy[:48]))+annual_ex_energy_cost)*np.ones(2)
        
        # box cost needs to not be hard coded
        years_of_project = 2
        box_build_cost = self.shell_cost + self.miner_number*self.miner_price
        dah = (self.shell_cost)/10 + (self.miner_number*self.miner_price)/years_of_project
        bus_tax = 0.19
        commercial_assessment = financials.financials(box_build_cost, gross_revenue, gross_cos, 
                                                      dah, bus_tax, years_of_project)
        endy = time.time()
        print("Elapsed after powerbox model = %s" % (endy - starty))
        end = time.time()
        results =  {"irr" : commercial_assessment.irr(), 
                    "moic" : commercial_assessment.moic(), 
                    "payback period" : commercial_assessment.payback_period(), 
                    "cash" : commercial_assessment.cash()[0],
                    "utilisation" : modely[1], 
                    "Elapsed time for pb_model (with compilation)" : (end - start)}
        return results

def form_data_parser(form_data):
    """ returns a dictionary of parameters coming from the web app form and modified to be compliant with Commercial Assessment module """
    # changed (1/1000) in front fo import cost to transform to kWh
    # need to change spill % to % 1-min var
    # duplicating data in miner power
    return {"file" : "Gigha_data_30_min.xlsx",
            "hh_factor": 1,
            "month_1_min" : 30*48*365/12,
            "month_hh" : 48*365/12, 
            "capacity" : float(form_data.get("rated_power")),
            "gen_energy_cost" : 0.05, 
            "imort_energy_cost" : (1/1000)*float(form_data.get("winter_op_price")),
            "data_cost" : 960, 
            "maintenance_cost" : float(form_data.get("powerbox_maintenance")),
            "security_cost" : 5000,
            "monitoring_cost" : 3333,
            "var" : (1/100)*float(form_data.get("spill")),
            "pb_load" : (1/1000)*float(form_data.get("miner_power"))*float(form_data.get("miner_number")), 
            "aux_load" : 7.4,
            "resolution" : 30,
            "miner_power" : (1/1000)*float(form_data.get("miner_power")), 
            "miner_terahash" : float(form_data.get("miner_hashing")),
            "export_revenue_per_e" : 0.05, 
            "miner_number" : float(form_data.get("miner_number")),
            "shell_cost" : float(form_data.get("powerbox_shell_cost")),
            "miner_price" : float(form_data.get("miner_price"))}