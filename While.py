from Execution import ExecutionHandler
from Portfolio import NaivePortfolio
from strategy import BuyandHoldStrategy
from Data import HistoricDataHandler
from Execution import SimulatedExecutionHandler
from Event import MarketEvent, SignalEvent, OrderEvent, fillEvent

import queue

if __name__ == "__main__":
    events = queue.Queue()
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
        #print(handler.get_latest_bars('AAPL'))