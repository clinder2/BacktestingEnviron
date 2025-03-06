from Environ.Execution import ExecutionHandler
from Environ.Portfolio import NaivePortfolio
from Environ.strategy import BuyandHoldStrategy
from Environ.Data import HistoricDataHandler
from Environ.Execution import SimulatedExecutionHandler
from Environ.Event import MarketEvent, SignalEvent, OrderEvent, fillEvent
from Environ.GA_SharpeStrategy import GA_SharpeStrategy
from Environ.MeanReversionStrategy import MRStrategy
from Environ.ModularPortfolio import MPortfolio

import queue

def While(assets, algo, start, end, init_Cap):
    q = queue.Queue()
    temp = HistoricDataHandler(q, start, end, assets)
    portfolio = MPortfolio(temp, q, start, init_Cap)
    strategy = None
    match algo:
        case 'GA':
            strategy = GA_SharpeStrategy(temp, q)
        case 'MA':
            strategy = MRStrategy(temp, q)
    executor = SimulatedExecutionHandler(q)
    testing = True
    i = 0
    while testing:
        i = i + 1
        #print('i: ' + str(i))
        temp.update_bars()
        if not temp.continue_backtest:
            testing = False
        while not q.empty():
            #print(str(i) + ', ' + str(temp.get_latest_bars('AAPL')))
            event = q.get()
            #print(event==None)
            #print(event.type)
            if event.type == 'MARKET':
                portfolio.update_timeindex(event)
                strategy.calculate_signals(event)
            elif event.type == 'SIGNAL':
                portfolio.update_signal(event)
            elif event.type == 'ORDER':
                executor.execute_order(event)
            elif event.type == 'FILL':
                portfolio.update_fill(event)
            #print(portfolio.current_holdings['cash'])
    #print('AAPL: ' + str(portfolio.current_holdings['AAPL']) + " NVDA: " + str(portfolio.current_holdings['NVDA']) + 
    #    ' IONQ: ' + str(portfolio.current_holdings['IONQ']))
    #print('AAPL: ' + str(portfolio.current_positions['AAPL']) + " NVDA: " + str(portfolio.current_positions['NVDA']) + 
    #    ' IONQ: ' + str(portfolio.current_positions['IONQ']))
    portfolio.create_tearsheet()
    print(portfolio.current_holdings['total'])

if __name__ == "__main__":
    While(['AAPL', 'NVDA'], 'MA', '2024-02-01', '2025-02-05', 1000)
    """ events = queue.Queue()
    handler = HistoricDataHandler(events, '2024-01-01', '2024-02-01', ['AAPL'])
    handler.update_bars()
    strategy = BuyandHoldStrategy(bars=handler, events=events)
    portfolio = NaivePortfolio(bars=handler, events=events, start_date='2024-01-01')
    executor = SimulatedExecutionHandler(events)
    i = 10
    while not events.empty() or i > 0:
        print(events.empty())
        i = i - 1
        if handler.continue_backtest:
            handler.update_bars()
        else:
            break
        while True:
            if events.empty():
                break
            else:
                event = events.get()
                if event is not None:
                    print(event.type)
                    if event.type == 'MARKET':
                        portfolio.update_timeindex(event)
                        strategy.calculate_signals(event)
                    elif event.type == 'SIGNAL':
                        portfolio.update_signal(event)
                    elif event.type == 'ORDER':
                        executor.execute_order(event)
                    elif event.type == 'FILL':
                        portfolio.update_fill(event)
        #print(portfolio.current_holdings)
        #print(handler.get_latest_bars('AAPL')) """