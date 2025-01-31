import datetime
import numpy as np
import pandas as pd
import matplotlib
import queue

from abc import ABCMeta, abstractmethod
from math import floor

from Event import fillEvent, OrderEvent

class Portfolio(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def update_signal(self, event):
        raise NotImplementedError("Error")
    
    @abstractmethod
    def update_fill(self, event):
        raise NotImplementedError("Error")
    
class NaivePortfolio(Portfolio):
    def __init__(self, bars, events, start_date, init_capital=1000000):
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events
        self.start_date = start_date
        self.init_capital = init_capital

        self.all_positions = self.construct_all_positions()
        self.current_positions = dict((k,v) for k,v in [(s,0) for s in self.symbol_list])
        self.all_holdings = self.construct_all_holdings()
        self.current_holdings = self.construct_current_holdings()

    def construct_all_positions(self):
        d = dict((k,v) for k,v in [(s,0) for s in self.symbol_list])
        d['datetime'] = self.start_date
        return [d]
    
    def construct_all_holdings(self):
        d = dict((k,v) for k,v in [(s,0) for s in self.symbol_list])
        d['datetime'] = self.start_date
        d['cash'] = self.init_capital
        d['commission'] = 0.0
        d['total'] = self.init_capital
        return [d]
    
    def construct_current_holdings(self):
        d = dict((k,v) for k,v in [(s,0) for s in self.symbol_list])
        d['cash'] = self.init_capital
        d['commission'] = 0.0
        d['total'] = self.init_capital
        return d
    
    def update_timeindex(self, event):
        bars = {}
        for s in self.symbol_list:
            bars[s] = self.bars.get_latest_bars(s, 1)
        d = dict((k,v) for k,v in [(s,0) for s in self.symbol_list])
        d['datetime'] = bars[self.symbol_list[0]][0][0]
        for s in self.symbol_list:
            d[s] = self.current_positions[s]
        self.all_positions.append(d)

        dh = dict((k,v) for k,v in [(s,0) for s in self.symbol_list])
        dh['datetime'] = bars[self.symbol_list[0]][0][0]
        dh['cash'] = self.current_holdings['cash']
        dh['commission'] = self.current_holdings['commission']
        dh['total'] = self.current_holdings['cash']

        for s in self.symbol_list:
            market_value = self.current_positions[s] * bars[s][0][1]
            dh[s] = market_value
            dh['total'] += market_value

        self.all_holdings.append(dh)
        self.current_holdings = dh # to update current holdings with timeindex

    def update_positions_from_fill(self, fill):
        fill_d = 0
        if fill.direction == 'BUY':
            fill_d = 1
        if fill.direction == 'SELL':
            fill_d = -1
        self.current_positions[fill.symbol] += fill_d * fill.quantity
    
    def update_holdings_from_fill(self, fill):
        fill_d = 0
        if fill.direction == 'BUY':
            fill_d = 1
        if fill.direction == 'SELL':
            fill_d = -1
        fill_cost = self.bars.get_latest_bars(fill.symbol)[0][1]
        cost = fill_d * fill_cost * fill.quantity
        self.current_holdings[fill.symbol] += cost
        self.current_holdings['commission'] += fill.commission
        self.current_holdings['cash'] -= (cost + fill.commission)
        self.current_holdings['total'] -= (cost + fill.commission)

    def update_fill(self, event):
        if event.type == 'FILL':
            self.update_positions_from_fill(event)
            self.update_holdings_from_fill(event)

    def generate_naive_order(self, signal):
        order = None

        symbol = signal.symbol
        direction = signal.signal_type
        #strength = signal.quantity
        strength = 1

        mkt_quantity = floor(100 * strength)
        curr_quantity = self.current_positions[symbol]
        order_type = 'MKT'

        if direction == 'LONG' and curr_quantity == 0:
            order = OrderEvent(symbol, order_type, mkt_quantity, 'BUY')
        if direction == 'SHORT' and curr_quantity == 0:
            order = OrderEvent(symbol, order_type, mkt_quantity, 'SELL')

        if direction == 'EXIT' and curr_quantity > 0:
            order = OrderEvent(symbol, order_type, abs(curr_quantity), 'SELL')
        if direction == 'EXIT' and curr_quantity < 0:
            order = OrderEvent(symbol, order_type, abs(curr_quantity), 'BUY')
        return order
    
    def update_signal(self, event):
        if event.type == 'SIGNAL':
            order_event = self.generate_naive_order(event)
            self.events.put(order_event)
    
    def create_equity_curve_dataframe(self):
        curve = pd.DataFrame(self.all_holdings)
        curve.set_index('datetime', inplace=True)
        curve['returns'] = curve['total'].pct_change()
        curve['equity_curve'] = (1.0+curve['returns']).cumprod()
        self.equity_curve = curve

    def create_tearsheet(self):
        self.create_equity_curve_dataframe()
        self.equity_curve['returns'].plot()