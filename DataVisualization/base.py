import numpy as np
import pandas as pd
import yfinance as yf

def retrieve_data(start, end, assets, freq, fields=['Dividends','Close','Open','Volume']):
    data = yf.download(assets, start, end, freq)
    header=pd.MultiIndex.from_product([fields, assets],names=['attr','asset'])
    inx=pd.date_range(start,end,freq='30min')
    print(data)
    dataset=pd.DataFrame(columns=header,index=inx)
    for f in fields:
        for a in assets:
            dataset.loc[:,(f,a)]=data[f][a]
    return dataset.dropna()

### add simple moving average to assets in original dataframe
def add_sma(frame, assets, win):
    for a in assets:
        frame.loc[:,('SMA',a)]=frame['Close'][a].rolling(win).mean().bfill()

### add volume weighted average price to assets in original dataframe
def add_vwap(frame,assets):
    for a in assets:
        frame.loc[:,('VWAP',a)]=np.cumsum(frame['Close'][a]*frame['Volume'][a])/np.cumsum(frame['Volume'][a])

if __name__=='__main__':
    data=retrieve_data("2025-01-1", "2025-10-10", ["AAPL", "NVDA", "IONQ", "PLTR"], '1h')
    add_sma(data, ['AAPL'], 30)
    add_vwap(data,['AAPL'])
    print(data)
    