# -*- coding:utf-8 -*-
# python for data analysis  8 economic data example 3 future
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import pandas_datareader as web
from datetime import datetime
# 建立转仓
px = web.get_data_yahoo('SPY', '2011-08-01', '2012-07-27')['Adj Close'] * 10
expiry = {'ESU2': datetime(2012, 9, 21),
          'ESZ2': datetime(2012, 12, 21)}
expiry = Series(expiry).sort_values()  # order 已被替换
# 利用Yahoo Finance的价格以及一个随机漫步和一些噪声模拟两份合约的未来走势
np.random.seed(12347)
N = 200
walk = (np.random.randint(0, 200, size=N) - 100) * 0.25
perturb = (np.random.randint(0, 20, size=N) - 10) * 0.25
walk = walk.cumsum()
rng = pd.date_range(px.index[0], periods=len(px) + N, freq='B')
near = np.concatenate([px.values, px.values[-1] + walk])
far = np.concatenate([px.values, px.values[-1] + walk + perturb])
prices = DataFrame({'ESU2': near, 'ESZ2': far}, index=rng)
# 将多个时间序列合并为单个连续序列：构造一个加权矩阵。活动合约的quanzhong
# 设为1， 直到期满为止。到期必须决定一个转仓约定。下面定义一个函数计算加权
# 矩阵（权重根据到期前的期数减小而线性衰减）
def get_roll_weights(start, expiry, items, roll_periods=5):
    # start : 用于计算加权矩阵的第一天
    # expiry : 由“合约代码->到期日期”组成的序列
    # items : 一组合约名称
    dates = pd.date_range(start, expiry[-1], freq='B')
    weights = DataFrame(np.zeros((len(dates), len(items))),
                        index=dates, columns=items)
    prev_date = weights.index[0]
    # expiry = Series([dates.values, dates.values], index=expiry.index)
    for i, (item, ex_date) in enumerate(expiry.iteritems()):
        if i < len(expiry) - 1:
            weights.ix[prev_date:ex_date - pd.offsets.BDay(), item] = 1
            roll_rng = pd.date_range(end=ex_date - pd.offsets.BDay(),
                                     periods=roll_periods + 1, freq='B')
            decay_weights = np.linspace(0, 1, roll_periods + 1)
            weights.ix[roll_rng, item] = 1 - decay_weights  # roll_rng可能会出现weights没有的日期
            weights.ix[roll_rng, expiry.index[i+1]] = decay_weights
        else:
            weights.ix[prev_date:, item] = 1
        prev_date = ex_date
    return weights
"""
    Starting in 0.20.0, the .ix indexer is deprecated,
    in favor of the more strict .iloc and .loc indexers.
"""
weights = get_roll_weights('6/1/2012', expiry, prices.columns)  # expiry只有合约与到期时间
rolled_returns = (prices.pct_change() * weights).sum(1)
print weights.ix['2012-09-12':'2012-09-21']
# 不能相乘,weights只到到期时间，prices模拟到了到期时间之后
print rolled_returns['2012-09-19']