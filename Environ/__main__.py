from Algorithms import *
from Environ.Execution import ExecutionHandler
from Environ.Portfolio import NaivePortfolio
from Environ.strategy import BuyandHoldStrategy
from Environ.Data import HistoricDataHandler
from Environ.Execution import SimulatedExecutionHandler
from Environ.Event import MarketEvent, SignalEvent, OrderEvent, fillEvent
from Environ.GA_SharpeStrategy import GA_SharpeStrategy
from Environ.MeanReversionStrategy import MRStrategy
from Environ.ModularPortfolio import MPortfolio
from Environ.While import While

import queue

While(['AAPL', 'NVDA', 'PLTR'], 'MA', '2025-01-01', '2025-04-08', 1000)

""" q = queue.Queue()
temp = HistoricDataHandler(q, "2025-01-01", "2025-02-04", ["AAPL", "NVDA", "IONQ", 'PLTR'])
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
portfolio.create_tearsheet()
print(portfolio.current_holdings['total']) """