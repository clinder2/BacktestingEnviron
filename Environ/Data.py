import pandas as pd
import datetime
import yfinance as yf
from queue import Queue
import matplotlib.pyplot as plt

from abc import ABCMeta, abstractmethod

from Environ.Event import MarketEvent

class DataHandler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_latest_bars(self, symbol, N=1):
        raise NotImplementedError("Not implemented")
    
    @abstractmethod
    def update_bars(self):
        raise NotImplementedError("Not implemented")
    
class HistoricDataHandler(DataHandler):
    """
    data handler to pull data from yfinance in interval (start, end)
    dates expected in format "yy-mm-dd"
    events = event queue
    symbol_list = requested symbols
    """
    def __init__(self, events, start, end, symbol_list):
        self.events = events
        self.start = start
        self.end = end
        self.symbol_list = symbol_list

        self.symbol_data = {}
        self.latest_symbol_data = {}
        self.continue_backtest = True

        self._pull_process_symbols()

    """
    pulls historic symbol_list data in range specified
    """
    def _pull_process_symbols(self):
        for s in self.symbol_list:
            data = yf.download(s, start = self.start, end=self.end, interval='1d')
            self.symbol_data[s] = {}
            data = pd.DataFrame(data)
            self.symbol_data[s] = data
            self.symbol_data[s]["returns"] = data["Close"].pct_change().dropna()
            self.latest_symbol_data[s] = []
            self.symbol_data[s] = self.symbol_data[s].itertuples()

    def _get_new_bar(self, symbol):
        #for t in self.symbol_data[symbol].itertuples():
        for t in self.symbol_data[symbol]:
            yield t

    def get_latest_bars(self, symbol, N=1):
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("error")
        else:
            return bars_list[-N:]
        
    def update_bars(self):
        for s in self.symbol_list:
            try:
                bar = self._get_new_bar(s).__next__()
            except StopIteration:
                self.continue_backtest = False
            else:
                if bar is not None:
                    self.latest_symbol_data[s].append(bar)
        self.events.put(MarketEvent())

    """ def BollingerPlot(self, symbol):
        lookback=10
        if len(self.latest_symbol_data[symbol]) >= lookback:
            print(self.latest_symbol_data[symbol])
            d = pd.DataFrame(self.latest_symbol_data[symbol]).rolling(lookback).mean()
            #upper = self.upper.dropna()
            #lower = self.lower.dropna()
            #plt.plot(upper)
            plt.plot(d)
            plt.show() """

if __name__ == "__main__":
    q = Queue()
    temp = HistoricDataHandler(q, "2024-01-01", "2024-02-01", ["AAPL", "NVDA", "IONQ"])
    for i in range(0, 10):
        temp.update_bars()
        print(temp.get_latest_bars('AAPL'))
    a = temp._get_new_bar("AAPL")
    #print(a)
    #print(a.__next__())
    #print(a.__next__())
    b = temp.latest_symbol_data["AAPL"]
    #print(temp.symbol_data['AAPL'])
    #print(a)
    #print(b[0][1])