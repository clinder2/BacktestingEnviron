import pandas as pd
from Data import HistoricDataHandler
from strategy import Strategy
from ModularPortfolio import MPortfolio
from Execution import SimulatedExecutionHandler
import sys
sys.path.append('/Users/christopherlinder/Desktop/MonteCarloFinance')
import matplotlib.pyplot as plt
#from MonteCarloFinance import GA_Sharpe_Fitness

from Event import SignalEvent, ComplexSignalEvent

import queue

"""
Strategy class with GA logic 
"""
class GA_SharpeStrategy(Strategy):

    def __init__(self, bars, events):
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events
        self.data = dict((k,v) for k,v in [(s, None) for s in self.symbol_list])
        for s in self.symbol_list:
            self.data[s] = self.bars.get_latest_bars(s, N=1)    # init database to price at instantiation

    def calculate_signals(self, event):
        if event.type == 'MARKET':
            for s in self.symbol_list:
                bars = self.bars.get_latest_bars(s, N=1)
                self.data[s].append(bars)   # update each symbol price on market event
            # Calculate optimal allocation
            for s in self.symbol_list:
                signal = ComplexSignalEvent(s, self.data[s][0][0], 1/len(self.symbol_list), 'GA')
                self.events.put(signal)

if __name__ == "__main__":
    q = queue.Queue()
    temp = HistoricDataHandler(q, "2025-01-01", "2025-01-28", ["AAPL", "NVDA", "IONQ"])
    #temp.update_bars()
    strategy = GA_SharpeStrategy(temp, q)
    portfolio = MPortfolio(temp, q, '2025-01-01', 1000)
    executor = SimulatedExecutionHandler(q)
    #print(strategy.data['AAPL'])
    first = True
    i = 0
    while first:
        i = i + 1
        print(i)
        temp.update_bars()
        if not temp.continue_backtest:
            first = False
        while not q.empty():
            event = q.get()
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
    portfolio.create_equity_curve_dataframe()
    portfolio.equity_curve['returns'].plot()
    plt.show()
    #for i in range(0, len(portfolio.all_holdings)):
    #    print('AAPL: ' + str(portfolio.all_holdings[i]['AAPL']))
    #print(strategy.data['AAPL'])
    #a = temp._get_new_bar("AAPL")
    #print(a)
    #print(a.__next__())
    #print(a.__next__())
    #print(temp.symbol_data['AAPL'])
    #print(a)
    #print(b[0][1])