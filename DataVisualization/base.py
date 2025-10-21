import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from pandas.tseries.offsets import BDay
import random

def retrieve_data(start, end, assets, freq, fields=['Close','Open','Volume']):
    data = yf.download(assets, start, end, interval=freq)
    header=pd.MultiIndex.from_product([fields, assets],names=['attr','asset'])
    inx=data.index
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

def vwap(group):
    return (group['Close']*group['Volume']).sum()/group['Volume'].sum()

def vwap_bymonth(frame: pd.DataFrame,assets):
    month_vwap=pd.DataFrame()
    month_vwap2=pd.DataFrame()
    month_vwap2.index=frame.index.copy()
    for a in assets:
        month_vwap2['Close']=frame['Close'][a]
        month_vwap2['Volume']=frame['Volume'][a]
        month_vwap[a]=month_vwap2.groupby([month_vwap2.index.year,month_vwap2.index.month]).apply(vwap)
    del month_vwap2
    return month_vwap

if __name__=='__main__':
    assets=["AAPL", "NVDA", "IONQ", "PLTR"]
    #data=retrieve_data("2024-01-1", "2025-10-10", ["AAPL",'IONQ','NVDA','PLTR'], '1h')
    #data2=retrieve_data("2025-09-1", "2025-10-10", ["AAPL"], '1h',fields=['Close'])
    # add_sma(data, ['AAPL'], 30)
    # add_vwap(data,['AAPL'])


    # ind=pd.date_range("2025-10-01", "2025-10-10",freq='1min')
    # index=ind[np.sort(np.random.choice(465,150))]
    # index2=ind[np.sort(np.random.choice(465,100))]
    # df=pd.DataFrame(columns=['tick'])
    # df['tick']=[random.choice(['AAPL', 'NVDA', 'IONQ', 'PLTR']) for _ in range(100)]
    # df['Close']=100*np.random.rand(100)
    # df['open']=10*np.random.rand(100)
    # df['Volume']=10000*np.random.rand(100)
    # df['time']=ind[:100]
    # df['day']=ind[:100].day
    # df.index=ind[:100]
    # quotes=pd.DataFrame(columns=['tick','bid','ask'])
    # quotes['tick']=[random.choice(['AAPL', 'NVDA', 'IONQ', 'PLTR']) for _ in range(150)]
    # quotes['bid']=10*np.random.rand(150)
    # quotes['ask']=quotes['bid'].values.copy()+np.random.rand(150)
    # quotes['time']=index.copy()
    # df['PnL']=(df['Close']-df['open'])/df['Volume']
    # print(df.groupby(['tick','day']).agg({'PnL': 'sum'}))
    # print(df.groupby(['tick','day']).agg({'PnL': 'mean'}))

    df=pd.DataFrame(columns=assets,index=pd.date_range('2025-10-1','2025-10-10',freq='1min'))
    for a in assets:
        df[a]=100*np.random.rand(df.index.shape[0])
    results=df.rolling(5).corr()
    print(results.tail())

    # cons={'A':pd.Timestamp('2024-10-01'),'B':pd.Timestamp('2025-8-01'),
    #       'C':pd.Timestamp('2025-9-20')}
    # A=pd.DataFrame(columns=['P'],index=pd.date_range('2024-10-01','2024-11-01',freq='B'))
    # #A.index=pd.date_range('2024-10-01','2024-12-01',freq='B')
    # A['P']=10*np.random.rand(A.index.shape[0])
    # B=pd.DataFrame(columns=['P'],index=pd.date_range('2025-8-01','2025-9-01',freq='B'))
    # #B.index=pd.date_range('2024-12-01','2025-8-01',freq='B')
    # B['P']=10*np.random.rand(B.index.shape[0])
    # C=pd.DataFrame(columns=['P'],index=pd.date_range('2025-9-20','2025-10-10',freq='B'))
    # #C.index=pd.date_range('2025-8-01','2025-9-01',freq='B')
    # C['P']=10*np.random.rand(C.index.shape[0])
    # fin=pd.DataFrame(columns=['P'],index=pd.date_range('2024-10-01','2025-10-10',freq='B'))
    # fin.loc[A.index]=A.values
    # fin.loc[B.index]=B.values
    # fin.loc[C.index]=C.values
    # d1=pd.date_range(A.index[-1]+BDay(),cons['B'],freq='B')
    # d2=pd.date_range(B.index[-1]+BDay(),cons['C'],freq='B')
    # a=np.linspace(1,0,d1.shape[0])
    # b=np.linspace(0,1,d1.shape[0])
    # fin.loc[d1]=np.reshape(A['P'][-1]*a+B['P'][0]*b,(d1.shape[0],1))
    # a=np.linspace(1,0,d2.shape[0])
    # b=np.linspace(0,1,d2.shape[0])
    # fin.loc[d2]=np.reshape(B['P'][-1]*a+C['P'][0]*b,(d2.shape[0],1))
    
    

    # data = {
    # 'symbol': ['AAPL','AAPL','AAPL','GOOG','GOOG'],
    # 'timestamp': [
    #     '2025-01-01 09:30:01', '2025-01-01 09:30:15', '2025-01-01 09:30:45',
    #     '2025-01-01 09:31:10', '2025-01-01 09:31:50'
    # ],
    # 'price': [182.1, 182.4, 182.2, 140.5, 140.8],
    # 'volume': [100, 50, 80, 200, 100]
    # }
    # df = pd.DataFrame(data)
    # df['timestamp'] = pd.to_datetime(df['timestamp'])
    # df=df.set_index('timestamp')
    # df=df.groupby('symbol').resample('5s').bfill()
    # df['vwap']=0.0
    # a=['AAPL','GOOG']
    # for t in a:
    #     temp=df.loc[t]
    #     temp=(temp['price']*temp['volume']).cumsum()/temp['volume'].cumsum()
    #     df.loc[df['symbol']==t,'vwap']=temp.values

    # df = pd.DataFrame({
    # 'symbol': ['AAPL','AAPL','AAPL','MSFT','MSFT'],
    # 'timestamp': pd.to_datetime([
    #     '2025-05-01 09:30:05', '2025-05-01 09:30:30', '2025-05-01 09:30:45',
    #     '2025-05-01 09:30:10', '2025-05-01 09:30:55'
    # ]),
    # 'price': [183.2, 183.4, 183.3, 315.5, 315.7],
    # 'volume': [200, 100, 150, 300, 250]
    # })
    # df['open']=0.0
    # df['close']=0.0
    # df['high']=0.0
    # df['low']=0.0
    # df=df.groupby('symbol').agg({
    #     'price':'ohlc',
    #     'volume':'sum'
    # })

    # prices = pd.DataFrame({
    # 'symbol': ['AAPL'] * 6,
    # 'timestamp': pd.date_range('2025-05-01 09:30', periods=6, freq='min'),
    # 'price': [183.2, 183.5, 183.7, 183.6, 183.9, 184.1]
    # })
    # prices['ret']=np.log(1+prices['price'].pct_change().bfill())
    # prices['vol_3min']=prices['ret'].rolling(3).std().bfill()
    
    # ticks = pd.DataFrame({
    # 'symbol': ['AAPL']*4 + ['MSFT']*4,
    # 'timestamp': pd.to_datetime([
    #     '2025-05-01 09:30:01','2025-05-01 09:31:00','2025-05-01 09:31:50','2025-05-01 09:34:30',
    #     '2025-05-01 09:30:10','2025-05-01 09:31:45','2025-05-01 09:32:00','2025-05-01 09:33:55'
    # ]),
    # 'Close': [183.1,183.2,183.4,183.6,315.1,315.3,315.2,315.5],
    # 'Volume': [100,200,150,120,200,250,300,150]
    # })
    # left=pd.DataFrame(index=pd.date_range('2025-05-01 09:30:00','2025-05-01 09:35:00',freq='1s'))
    # left['timestamp']=left.index.copy()
    # ticks=ticks.set_index('timestamp')
    # ticks=ticks.groupby('symbol').resample('1min').apply(vwap)
    
    # ticks = pd.DataFrame({
    # 'symbol': ['AAPL']*4,
    # 'timestamp': pd.to_datetime(['09:30:01','09:30:15','09:30:45','09:31:05']),
    # 'price': [183.2,183.3,183.4,183.5]
    # })
    # signals = pd.DataFrame({
    #     'symbol': ['AAPL']*2,
    #     'timestamp': pd.to_datetime(['09:30:00','09:31:00']),
    #     'signal': [0.1, 0.15]
    # })
    # result=pd.merge_asof(ticks,signals,by='symbol',on='timestamp',direction='backward')
    
    # data = {
    # 'symbol': ['AAPL'] * 5,
    # 'timestamp': pd.date_range('2025-05-01 09:30', periods=5, freq='T'),
    # 'price': [183.1, 183.15, 183.5, 184.0, 183.2]
    # }
    # df = pd.DataFrame(data)
    # df['pct']=df['price'].pct_change().bfill()
    
    # rets = pd.DataFrame({
    # 'timestamp': pd.date_range('2025-05-01 09:30', periods=6, freq='T'),
    # 'AAPL': [0.001, 0.002, -0.001, 0.000, 0.002, 0.001],
    # 'MSFT': [0.000, 0.001, -0.002, 0.001, 0.001, 0.002]
    # })
    # rets['corr']=rets['AAPL'].rolling(3).corr(rets['MSFT'])
    
    # daily = pd.DataFrame({
    # 'symbol': ['AAPL']*5,
    # 'date': pd.date_range('2025-04-28', periods=5, freq='B'),
    # 'close': [182.0, 183.0, 183.5, 182.2, 184.0]
    # })
    # daily['gap']=(daily['close'].shift(-1)-daily['close']-.3)/daily['close'].shift(-1)

    # data = {
    # 'timestamp': pd.date_range('2025-05-01 09:30:00', periods=5, freq='10S'),
    # 'price': [183.1, 183.2, 183.3, 183.5, 183.4]
    # }
    # df = pd.DataFrame(data)
    # df=df.set_index('timestamp')
    # df=df.resample('1S').ffill()

    # data = pd.DataFrame({
    # 'timestamp': pd.date_range('2025-05-01 09:30', periods=6, freq='T'),
    # 'AAPL': [183.2, 183.5, 183.7, 183.6, 183.9, 184.1],
    # 'SPY': [512.0, 512.2, 512.5, 512.3, 512.9, 513.0]
    # })
    # data['ar']=data['AAPL'].pct_change().bfill()
    # data['sr']=data['SPY'].pct_change().bfill()
    # data['beta']=(data['ar'].rolling(3).cov(data['sr'])/data['sr'].rolling(3).var()).bfill()
    
    # df = pd.DataFrame({
    # 'symbol': ['AAPL']*6,
    # 'timestamp': pd.date_range('2025-05-01 09:30', periods=6, freq='T'),
    # 'volume': [100, 120, 130, 900, 110, 115]
    # })
    # m=df['volume'].mean()
    # s=df['volume'].std()
    # print(df.loc[df['volume']>m+2*s])