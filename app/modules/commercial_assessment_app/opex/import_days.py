# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 10:18:56 2020

@author: PeterParker
"""

def import_days(df, aux_load, p_to_E_conv):
    aux_import = df[df.values < aux_load]
    import_days = len(aux_import)/(24/p_to_E_conv)
    return import_days
    