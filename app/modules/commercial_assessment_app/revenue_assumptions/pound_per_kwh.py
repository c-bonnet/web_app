# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 16:24:01 2020

@author: Chae Gordon
"""

"""
Pound per kWh (Revenue Assumption) Calculator
This method calculates the £/kWh of a mining instance.
Inputs:
    Power: the power draw of a miner in kW
    Mining Power: The hashing power in TH/s
    
"""
import requests
import json

def pounds_per_kwh(power, mining_power, btc_reward_block=12.5):
    # get the stats using the inputs module
    stats_url =  "https://api.blockchain.info/stats"
    api_json = requests.get(stats_url)
    data = json.loads(api_json.text)
    market_price_btc = data["market_price_usd"]
    difficulty_btc = data["difficulty"]
    
    # get $ to £ conversion (ie. times $ by this to get £)
    exchange_url = "https://api.exchangeratesapi.io/latest"
    exchange_json =  requests.get(exchange_url)
    exchange_data = json.loads(exchange_json.text)["rates"]
    dollar_to_pound = exchange_data["GBP"]/exchange_data["USD"]
    
    # The terahashes required to mine a block
    terahashes = 10**12
    th_per_block = difficulty_btc*(2**32)/terahashes
    
    # the terahashes per pound
    th_per_btc = th_per_block/btc_reward_block
    th_per_dollar = th_per_btc/market_price_btc
    th_per_pound = th_per_dollar/dollar_to_pound
    
    # the kWh per terahash
    efficiency = power/mining_power  # kW/THs^-1 or kJ/TH
    joule_to_kwh = (60**2)  # number of J in a kWh
    efficiency_kwh =  efficiency/joule_to_kwh  # kWh/TH
    
    # want the £/TH and the kWh/TH --> £/kWh = (£/TH)/(kWh/TH)
    pound_per_kwh = (1/th_per_pound)/efficiency_kwh
    
    return pound_per_kwh
