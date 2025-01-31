import datetime
import numpy as np
import pandas as pd
import queue

from abc import ABCMeta, abstractmethod

from Event import SignalEvent

class Strategy(object):
    __metaclass__ = ABCMeta

    def calculate_signals(self):
        raise NotImplementedError("error")
    
class BuyandHoldStrategy(Strategy):
    """
    bars is DataHandler to provide bar information
    event is queue of events
    """
    def __init__(self, bars, events):
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events

        self.bought = self._calculate_initial_bought()

    def _calculate_initial_bought(self):
        bought = {}
        for s in self.symbol_list:
            bought[s] = False
        return bought
    
    def calculate_signals(self, event):
        if event.type == 'MARKET':
            for s in self.symbol_list:
                bars = self.bars.get_latest_bars(s,N=1)
                if bars is not None and bars != []:
                    if self.bought[s] == False:
                        print("buying")
                        signal = SignalEvent(s, bars[0][0], 'LONG')
                        self.events.put(signal)
                        self.bought[s] = True