'''
/**
 * real_time_global_orderbook.py
 * 
 * Streams a real-time orderbook for the supplied pair
 * An example of the real-time orderbook is available here:
 * https://app.ae3platform.com/markets/p/BTC/USDT
 * 
 * Disclaimer:
 * APEX:E3 is a financial technology company based in the United Kingdom https://www.apexe3.com
 *  
 * None of this code constitutes financial advice. APEX:E3 is not 
 * liable for any loss resulting from the use of this code or the API. 
 * 
 * This code is governed by The MIT License (MIT)
 * 
 * Copyright (c) 2020 APEX:E3 Team
 * 
 **/
'''

import sys
sys.path.append('..')
from apexe3.apexe3 import initialise
from apexe3.apexe3 import initialise_stream
from apexe3.apexe3 import initialise_global_orderbook
import datetime

import pandas as pd
    #Cumulative has a bug - only show bid px  bid size  bid sum

EXCHANGES = ['FTX', 'COINBASEPRO']

def process_global_orderbook(event):
    with open('./data/bid.csv', 'a') as f1, open('./data/ask.csv', 'a') as f2:
        now = x = datetime.datetime.now().replace(microsecond=0)
        if now.second % 5 > 5:
            return 
        table=pd.DataFrame(event["bids"])
        table.columns = ['bid px', 'bid size', 'bid size cumulative', 'bid sum', 'bid sum cumulative', 'exchange']
        L = min(20, table.shape[0])
        table = table[:L]
        table['time'] = [now] * L
        # table.to_csv(f1, header=False)
        print(table)
        bestBid = table['bid px'][0]
        
        table=pd.DataFrame(event["asks"])
        table.columns = ['ask px', 'ask size', 'ask size cumulative', 'ask sum', 'ask sum cumulative', 'exchange']
        L = min(20, table.shape[0])
        table = table[:L]
        table['time'] = [now] * L
        # table.to_csv(f2, header=False)
        print(table)
        bestAsk = table['ask px'][0]
        print(bestBid, bestAsk, bestAsk - bestBid)


def init():
    with open('./../secret.txt', 'r') as f:
        clientId = f.readline().strip()
        clientSecret = f.readline().strip()
    f.close()
    emitter = initialise(clientId, clientSecret)
    emitter.on('GLOBAL_ORDERBOOK', process_global_orderbook)


if __name__ == "__main__":
    init()
    #Change these values to a base or quote you are interested in
    initialise_global_orderbook("btc", "usdt", EXCHANGES,"SPOT")

  