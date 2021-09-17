# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 15:15:17 2021

####################################
### DHP TRADING STRATEGY  ##########
####################################


@author: AndyAlves
"""

import pandas as pd
import ta as techa
import talib
import matplotlib.pyplot as plt
import datetime as dt

# Variables
timeframe = '1d'
start_date = '2016-01'
end_date = '2020-12'

def get_banknifty_data(local = True) : 
    if local == True:
        data = pd.read_csv("D:\Qbatomic\Datas\TimeSeries\Banknifty\Intraday_1_Min_Data\intraday_1m_data_after_consolidation\BNF\\bnf_2016-2020_intraday_1m.txt", parse_dates=True)
        data.drop(['useless1','useless2'], axis=1, inplace = True)
        return data
    else:
        print("No API spcified")
        return
    
def plot_subplot (ax1_data, macd_data) :
    #PLOTTING MACD 
    ax1 = plt.subplot2grid((8,1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((8,1), (5,0), rowspan = 3, colspan = 1)
    
    ax1.plot(ax1_data['close'], color = 'skyblue', linewidth = 2, label = 'Banknnifty')
    ax1.legend()
    ax1.set_title('BNF MACD SIGNALS')
    ax2.plot(macd_data['macd'], color = 'grey', linewidth = 1.5, label = 'MACD')
    ax2.plot(macd_data['signal'], color = 'skyblue', linewidth = 1.5, label = 'SIGNAL')
    
    
    for i in range(len(macd_data)):
        if str(macd_data['histogram'][i])[0] == '-':
            ax2.bar(macd_data.index[i], macd_data['histogram'][i], color = '#ef5350')
        else:
            ax2.bar(macd_data.index[i], macd_data['histogram'][i], color = '#26a69a')
            
    plt.legend(loc = 'upper left')
    plt.show()
    
def find_returs_from_trades(trade_dict):
   df_profits = []    
   for i in trades['trades']:
        #print(i[0]['type'])
        if len(i) == 2 :
            if i[0]['type'] == 'entry long':
               profit = i[1]['price'] - i[0]['price']
               df_profits.append(profit)
            elif i[0]['type'] == 'entry short':
                profit = i[0]['price'] - i[1]['price']
                df_profits.append(profit)
   return df_profits   

def Cumulative(lists):
    cu_list = []
    length = len(lists)
    cu_list = [sum(lists[0:x:1]) for x in range(0, length+1)]
    return cu_list[1:]
    
    
# GET BANKNIFTY DATA AND Process data into right DF 
bnf_data = get_banknifty_data().drop(["ticker"] ,axis=1)
bnf_data["Date"] = bnf_data["Date"].astype(str) + '-' + bnf_data["time"].astype(str)
bnf_data['Date'] = pd.to_datetime(bnf_data["Date"] , format = "%Y%m%d-%H:%M")
bnf_data.drop(['time'], inplace = True, axis = 1)
bnf_data.set_index('Date', inplace = True)
print(bnf_data.duplicated(subset=None, keep='first'))

#Resample Data and generate MACD values
bnf_resample = bnf_data[start_date : end_date]['close'].resample(timeframe).ohlc().dropna()
bnf_resample.reset_index(inplace = True)
macd, macdsignal, macdhist = talib.MACD(bnf_resample['close'], fastperiod=12, slowperiod=26, signalperiod=9)
macd_data = pd.DataFrame({'Date' : bnf_resample['Date'], 'macd' : macd, 'signal' : macdsignal, 'histogram' : macdhist})
plot_subplot(bnf_resample, macd_data)

# Create trading signals based on MACD indicator
trades = {"trades" :[]}
last_position = 'none'
last_trade = None
for i in range(len(bnf_resample)) :
   if (macd_data.loc[i, 'macd'] > macd_data.loc[i, 'signal']):
       
       if last_trade is None or last_trade == 'exit long' or last_trade == 'exit short' :
           trade = [{'type' : 'entry long', 'price' : bnf_resample.loc[i, 'close'], 'time' : bnf_resample.loc[i, 'Date']}]
           trades['trades'].append(trade)
           last_trade = 'entry long'
       elif last_trade == 'entry short' :
           trade = {'type' : 'exit short', 'price' : bnf_resample.loc[i, 'close'], 'time' : bnf_resample.loc[i, 'Date']}
           trades['trades'][-1].append(trade)
           last_trade = 'exit short'
             
   elif(macd_data.loc[i, 'macd'] < macd_data.loc[i, 'signal'] and last_position != 'sell'):
       
        if last_trade is None or last_trade == 'exit long' or last_trade == 'exit short' :
           trade = [{'type' : 'entry short', 'price' : bnf_resample.loc[i, 'close'], 'time' : bnf_resample.loc[i, 'Date']}]
           trades['trades'].append(trade)
           last_trade = 'entry short'
        elif last_trade == 'entry long' :
            trade = {'type' : 'exit long', 'price' : bnf_resample.loc[i, 'close'], 'time' : bnf_resample.loc[i, 'Date']}
            trades['trades'][-1].append(trade)
            last_trade = 'exit long'
       

profits = find_returs_from_trades(trades)
pd.Series(Cumulative(profits)).plot()



