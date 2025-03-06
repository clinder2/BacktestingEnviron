import numpy as np
from Environ.Portfolio import NaivePortfolio

from Environ.Event import ComplexSignalEvent, OrderEvent

class MPortfolio(NaivePortfolio):
    def generate_order(self, signal):
        order = None
        symbol = signal.symbol
        algo = signal.signal_type

        ord_quantity = signal.quantity
        curr_quantity = self.current_positions[symbol]
        order_type = 'MKT'

        if algo == 'GA':
            print(self.current_holdings['total'])
            allocation = ord_quantity * self.current_holdings['total']
            diff = self.current_holdings[symbol] - allocation
            cost = self.bars.get_latest_bars(symbol)[0][1]
            quantity = np.floor(np.abs(diff/cost))
            if allocation < self.current_holdings[symbol]:
                order = OrderEvent(symbol, order_type, quantity, 'SELL')
                print(str(symbol) + " sell, " + str(quantity) + ", cost: " + str(cost) + ", " + str(allocation))
            else:
                order = OrderEvent(symbol, order_type, quantity, 'BUY')
                print(str(symbol) + " buy, " + str(quantity) + ", cost: " + str(cost) + ", " + str(allocation))
        elif algo == 'MR':
            #print(ord_quantity)
            #cost = self.bars.get_latest_bars(symbol)[0][1]
            if ord_quantity == 1:
                order = OrderEvent(symbol, order_type, 1, 'BUY')
            else:
                order = OrderEvent(symbol, order_type, 0 if curr_quantity==0 else 1, 'SELL')

        """ if direction == 'LONG' and curr_quantity == 0:
            order = OrderEvent(symbol, order_type, ord_quantity, 'BUY')
        if direction == 'SHORT' and curr_quantity == 0:
            order = OrderEvent(symbol, order_type, ord_quantity, 'SELL')

        if direction == 'EXIT' and curr_quantity > 0:
            order = OrderEvent(symbol, order_type, abs(curr_quantity), 'SELL')
        if direction == 'EXIT' and curr_quantity < 0:
            order = OrderEvent(symbol, order_type, abs(curr_quantity), 'BUY') """
        return order
    
    def update_signal(self, event):
        if event.type == 'SIGNAL':
            order_event = self.generate_order(event)
            self.events.put(order_event)