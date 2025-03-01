import pandas as pd
import numpy as np
from Data import HistoricDataHandler
from strategy import Strategy
from ModularPortfolio import MPortfolio
from Execution import SimulatedExecutionHandler
import sys
sys.path.insert(0, '/Users/christopherlinder/Desktop/MonteCarloFinance/UtilityFunctions/GA_Sharpe_Fitness')
import matplotlib.pyplot as plt

from Event import SignalEvent, ComplexSignalEvent

import queue

class MRStrategy(Strategy):

    def __init__(self, bars, events):
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events
        self.data = dict((k,v) for k,v in [(s, None) for s in self.symbol_list])
        self.M = dict((k,v) for k,v in [(s, 0) for s in self.symbol_list])
        self.upper = dict((k,v) for k,v in [(s, 0) for s in self.symbol_list])
        self.lower = dict((k,v) for k,v in [(s, 0) for s in self.symbol_list])
        for s in self.symbol_list:
            self.data[s] = self.bars.get_latest_bars(s)    # init database to price at instantiation

    def calculate_signals(self, event):
        if event.type == 'MARKET':
            for s in self.symbol_list:
                bars = self.bars.get_latest_bars(s, N=1)[0][1]
                self.data[s].append(bars)   # update each symbol price on market event
            for s in self.symbol_list:
                self.updateSMA(s)
            for s in self.symbol_list:
                self.upper[s] = (self.M[s] + 2*pd.DataFrame(self.data[s]).rolling(10).std()).iloc[-1].item()
                self.lower[s] = (self.M[s] - 2*pd.DataFrame(self.data[s]).rolling(10).std()).iloc[-1].item()
                #print('upper: ' + str(self.upper[s]))
                cost = self.bars.get_latest_bars(s)[0][1]
                signal=None
                #print('M: ' + str(self.M[s]))
                #print('U: ' + str(self.upper[s]))
                #print('L: ' + str(self.lower[s]))
                if self.upper[s] <= cost:
                    print("s")
                    signal = ComplexSignalEvent(s, self.bars.get_latest_bars(s, N=1)[0][0], -1, 'MR')
                elif self.lower[s] >= cost:
                    print('b')
                    signal = ComplexSignalEvent(s, self.bars.get_latest_bars(s, N=1)[0][0], 1, 'MR')
                if signal != None:
                    self.events.put(signal)

    def updateSMA(self, symbol):
        lookback=10
        if len(self.data[symbol]) >= lookback:
            d = pd.DataFrame(self.data[symbol]).rolling(lookback).mean()
            self.M[symbol] = d.iloc[-1].item()
            """ n=np.array(self.data[symbol][-lookback:])
            sa = n.sum()/lookback
            self.M[symbol] = (self.M[symbol]+sa)/(len(self.M[symbol])+1) """
    
    def updateWMA(self, symbol):
        lookback=10
        if len(self.data[symbol]) >= lookback:
            """ w=np.arange(1, lookback+1)
            n=self.data[symbol][-lookback:]
            print(n)
            wma = np.dot(w, n)
            self.M[symbol] += wma """
            data = pd.DataFrame(self.data[symbol])
            w = np.arange(1, lookback+1)
            wma = data.rolling(len(w)).apply(lambda x: np.dot(x, w)/w.sum())
            return wma
    
    def updateMA(self, symbol, type):
        if type == 'sma':
            self.updateSMA(symbol)
        elif type =='wma':
            self.updateWMA(symbol)

    def BollingerPlot(self, symbol):
        upper = self.upper.dropna()
        lower = self.lower.dropna()
        plt.plot(upper)
        plt.show()

if __name__ == "__main__":
    q = queue.Queue()
    temp = HistoricDataHandler(q, "2025-01-01", "2025-02-28", ["AAPL", "NVDA", "IONQ", 'PLTR'])
    #temp.update_bars()
    strategy = MRStrategy(temp, q)
    portfolio = MPortfolio(temp, q, '2025-01-01', 1000)
    executor = SimulatedExecutionHandler(q)
    #print(strategy.data['AAPL'])
    first = True
    i = 0
    while first:
        i = i + 1
        print('i: ' + str(i))
        temp.update_bars()
        if not temp.continue_backtest:
            first = False
        while not q.empty():
            event = q.get()
            #print(event==None)
            print(event.type)
            if event.type == 'MARKET':
                portfolio.update_timeindex(event)
                strategy.calculate_signals(event)
            elif event.type == 'SIGNAL':
                portfolio.update_signal(event)
            elif event.type == 'ORDER':
                #print(str(event.direction) + ", " + str(event.symbol))
                executor.execute_order(event)
            elif event.type == 'FILL':
                portfolio.update_fill(event)
            #print(portfolio.current_holdings['cash'])
    print('AAPL: ' + str(portfolio.current_holdings['AAPL']) + " NVDA: " + str(portfolio.current_holdings['NVDA']) + 
        ' IONQ: ' + str(portfolio.current_holdings['IONQ']))
    print('AAPL: ' + str(portfolio.current_positions['AAPL']) + " NVDA: " + str(portfolio.current_positions['NVDA']) + 
        ' IONQ: ' + str(portfolio.current_positions['IONQ']))
    #portfolio.create_tearsheet()
    print(portfolio.current_holdings['total'])