# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 15:15:17 2021

####################################
### DHP TRADING STRATEGY  ##########
####################################


@author: AndyAlves
"""

import pandas as pd
import datetime as dt


def get_banknifty_data(local = True) : 
    if local == True:
        data = pd.read_csv("D:\Qbatomic\Datas\TimeSeries\Banknifty\Intraday_1_Min_Data\intraday_1m_data_after_consolidation\BNF\\bnf_2016-2020_intraday_1m.txt")
        data.drop(['useless1','useless2'], axis = 1)
        return data
        
        
bnf_data = get_banknifty_data()
