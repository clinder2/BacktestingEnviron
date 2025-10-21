import queue
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

### Vectorized mini-backtester

class Event(object):
    def __init__(self):
        pass

class TickEvent(Event):
    def __init__(self, data: pd.DataFrame):
        self.tick=data['tick']
        self.bid=data['open']

class OrderEvent(Event):
    def __init__(self, type: str, side: str):
        self.type=type
        self.side=side

class Strategy(object):
    def __init__(self):
        pass

class MACrossoverStrategy(Strategy):
    def __init__(self, events: queue, assets: list, bars: pd.DataFrame, 
                 longw: int, shortw: int):
        self.events=events
        self.assets=assets
        self.bars=bars
        self.longw=longw
        self.shortw=shortw

    def calculate_signals(self, subset: list):
        signals=pd.DataFrame(columns=subset, index=self.bars.index)
        for a in subset:
            wins=pd.DataFrame(columns=['l', 's'],index=signals.index)
            if a in self.assets:
                signals[a]=0
                wins['l']=self.bars[a].rolling(self.longw).mean()
                wins['s']=self.bars[a].rolling(self.shortw).mean()
                signals.loc[wins['s']>wins['l'],a]=1
                signals.loc[wins['s']<wins['l'],a]=0
                signals[a+'-s']=signals[a].diff()
        return signals
    
class Portfolio(object):
    def __init__(self):
        pass

class MACrossoverPortfolio(Portfolio):
    def __init__(self, bars, signals, assets):
        self.bars=bars
        self.signals=signals
        self.assets=assets

    def generate_holdings(self):
        self.positions=pd.DataFrame(columns=self.assets, index=self.signals.index.copy())
        for a in self.assets:
            self.positions[a]=100*self.signals[a]
    
    def backtest(self):
        self.results=pd.DataFrame(index=self.signals.index.copy())
        self.results['total']=0
        self.results['cash']=0
        for a in self.assets:
            temp=(self.positions[a]*self.bars[a])
            self.results[a]=temp
            self.results['total']+=temp
            self.results['cash']=-(self.signals[a+'-s']*self.bars[a]).cumsum()

if __name__=='__main__':
    assets=["AAPL",'IONQ','NVDA','PLTR']
    bars=yf.download("2025-01-1", "2025-10-10", assets, '1h')
    # bars=pd.read_csv('DataVisualization/test3.csv')
    # bars2=pd.DataFrame(columns=assets)
    # i=0
    # for a in assets:
    #     bars2[a]=bars['Close'+ ('' if a=='AAPL' else '.'+str(i))][2:].astype(float)
    #     i+=1
    # bars2.index=pd.to_datetime(bars['Price'][2:])
    # bars=bars2
    events=queue.Queue()
    strategy=MACrossoverStrategy(events, assets, bars, 40, 10)
    signals=strategy.calculate_signals(assets)
    portfolio=MACrossoverPortfolio(bars, signals, assets)
    portfolio.generate_holdings()
    portfolio.backtest()
    portfolio.results['AAPL'].plot()
    portfolio.results['NVDA'].plot()
    plt.show()