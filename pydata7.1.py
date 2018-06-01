# -*- coding:utf-8 -*-
# python for data analysis  8 economic data example 1
import numpy as np
import pandas as pd
from pandas import Series
import matplotlib.pyplot as plt
import pandas_datareader as web
data = web.get_data_yahoo('SPY', '2006-01-01', '2012-07-27')
# 计算日收益率，并将收益率变换为趋势信号（通过滞后移动形成）
px = data['Adj Close']
returns = px.pct_change()


def to_index(rets):
    index = (1 + rets).cumprod()
    p = list(index.index)
    first_loc = max(p.index(index.notnull().argmax()) - 1, 0)  # index.notnull().argmax()返回为时间戳
    index.values[first_loc] = 1
    return index


def trend_signal(rets, lookback, lag):
    signal = Series.rolling(rets, lookback, min_periods=lookback - 5).sum()
    return signal.shift(lag)
"""
    FutureWarning: pd.rolling_sum is deprecated for Series
    and will be removed in a future version, replace with
    Series.rolling(min_periods=95,window=100,center=False).sum()
"""
# 创建和测试一种根据每周五动量信号进行交易的交易策略
signal = trend_signal(returns, 100, 3)
trade_friday = signal.resample('W-FRI').resample('B').ffill()  # 升采样
trade_rets = trade_friday.shift(1)*returns
to_index(trade_rets).plot()
# 该策略性能按不同大小的交易波幅进行划分。年度标准差是计算波幅的一种方法
# 我们可以通过计算夏普比率来观察不同波动机制下的风险收益率
vol = Series.rolling(returns, 250, min_periods=200).std() * np.sqrt(250)
vol = vol[trade_rets.index].ffill()
def sharpe(rets, ann=250):
    return rets.mean() /rets.std() * np.sqrt(ann)
# trade_rets升采样数据量与vol不同
trade_rets = trade_rets.groupby(pd.qcut(vol, 4)).agg(sharpe)
print trade_rets

