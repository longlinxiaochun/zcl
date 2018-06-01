# -*- coding:utf-8 -*-
# python for data analysis  8 economic data example 2
import numpy as np
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import pandas_datareader as web
from collections import defaultdict
names = ['AAPL', 'GOOG', 'MSFT', 'GS', 'MS', 'BAC', 'C']


def get_px(stock, start, end):
    return web.get_data_yahoo(stock, start, end)['Adj Close']
px = DataFrame({n: get_px(n, '2009-01-01', '2012-01-06')for n in names})
px = px.asfreq('B').fillna(method='pad')
# 每只股票累计收益
rets = px.pct_change()
# 构建投资组合，计算特定回顾期的动量，并按降序排列


def calc_mom(price, lookback, lag):
    mom_ret = price.shift(lag).pct_change(lookback)
    ranks = mom_ret.rank(axis=1, ascending=False)
    ranks_mean = ranks.mean(axis=1)
    n = len(ranks_mean)
    demeaned_value = ranks.values - ranks_mean.values.reshape(n, 1)   # DataFrame因为列名不同无法广播
    demeaned_values = demeaned_value / demeaned_value.std(axis=1).reshape(n, 1)
    demeaned = DataFrame(demeaned_values, columns=ranks.columns, index=ranks.index)
    return demeaned
# 对策略进行事后检验：通过指定回顾期和持有期计算投资组合整体的夏普比率
compound = lambda x: (1+x).prod() - 1
daily_sr = lambda x: x.mean() / x.std()


def strat_sr(prices, lb, hold):
    # 计算投资组合权重
    freq = '%dB' % hold
    port = calc_mom(prices, lb, lag=1)
    daily_rets = prices.pct_change()
    # 计算投资组合收益
    port = port.shift(1).resample(freq, how='first')
    returns = daily_rets.resample(freq, how=compound)
    port_rets = (port * returns).sum(axis=1)
    return daily_sr(port_rets) * np.sqrt(252 / hold)

lookbacks = range(20, 90, 5)
holdings = range(20, 90, 5)
dd = defaultdict(dict)
for lb in lookbacks:
    for hold in holdings:
        dd[lb][hold] = strat_sr(px, lb, hold)
ddf = DataFrame(dd)
ddf.index.name = 'Holding Period'
ddf.columns.name = 'Lookback Period'
# 结果图形化，生成热图


def heatmap(df, cmap=plt.cm.gray_r):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    axim = ax.imshow(df.values, cmap=cmap, interpolation='nearest')
    ax.set_xlabel(df.columns.name)
    ax.set_xticks(np.arange(len(df.columns)))
    ax.set_xticklabels(list(df.columns))
    ax.set_ylabel(df.index.name)
    ax.set_yticks(np.arange(len(df.index)))
    ax.set_yticklabels(list(df.index))
    plt.colorbar(axim)
heatmap(ddf)
plt.show()