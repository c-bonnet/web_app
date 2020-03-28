# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 15:56:34 2020

@author: PeterParker
"""

# to begin with will have persistent modelling on market forces

import requests 
import json

"""Code to gather difficulty and price of BTC"""

def get_stats():
    stats_url =  "https://api.blockchain.info/stats"
    api_json = requests.get(stats_url)
    data = json.loads(api_json.text)
    btc_price = data["market_price_usd"]
    btc_difficulty = data["difficulty"]
    return btc_price*get_dollar_to_pound(), btc_difficulty
    
def get_dollar_to_pound():
    dollar_url =  "https://api.exchangeratesapi.io/latest"
    api_json = requests.get(dollar_url)
    data = json.loads(api_json.text)
    rates = data["rates"]
    dollar_to_pound = rates["GBP"]/rates["USD"]
    return dollar_to_pound