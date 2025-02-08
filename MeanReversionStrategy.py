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
        for s in self.symbol_list:
            self.data[s] = self.bars.get_latest_bars(s)    # init database to price at instantiation

    def calculate_signals(self, event):
        if event.type == 'MARKET':
            t = []
            for s in self.symbol_list:
                t.append(self.WMA(s))
    
    def WMA(self, symbol):
        data = pd.DataFrame(self.data[symbol])
        w = np.arange(1, len(data)+1)
        wma = data.rolling(len(w)).apply(lambda x: np.dot(x, w)/w.sum())
        return wma
