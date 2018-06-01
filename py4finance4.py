# -*- coding: utf-8 -*-
import warnings
import pymc as pm
import numpy as np
import matplotlib.pyplot as plt
warnings.simplefilter('ignore')
np.random.seed(1000)
x = np.linspace(0, 10, 500)
y = 4 + 2 * x + np.random.standard_normal(len(x)) * 2
# 最小二乘回归
reg = np.polyfit(x, y, 1)
plt.figure(figsize=(8, 4))
plt.scatter(x, y, c=y, marker='v')
plt.plot(x, reg[1] + reg[0] * x, lw=2.0)
plt.colorbar()
plt.grid(True)
plt.xlabel('x')
plt.ylabel('y')

# Bayesian Regression
# with无法使用，pm.Model中没有__enter__与__exit__结构
with pm.Model() as model:
    # define priors
    alpha = pm.Normal('alpha', mu=0, sd=20)
    beta = pm.Normal('beta', mu=0, sd=20)
    sigma = pm.Uniform('sigma', lower=0, upper=10)
    # define linear regression
    y_est = alpha + beta * x
    # define likelihood
    likelihood = pm.Normal('y', mu=y_est, sd=sigma, observed=y)
    # inference
    start = pm.find_MAP()
    # find starting value by optimization
    step = pm.NUTS(state=start)
    # instantiate MCMC sampling algorithm
    trace = pm.sample(100, step, start=start, progressbar=False)
    # draw 100 posterior samples using NUTS sampling

fig = pm.traceplot(trace, lines={'alpha': 4, 'beta': 2, 'sigma': 2})
plt.figure(figsize=(8, 8))


#  GUI
# 出现NotImplementedError，被调用却没被实现,需要用到pyqt4
# 使用Anaconda新版本会强制安装pyqt5，如不兼容则卸载重装pyqt4
import numpy as np
import traits.api as trapi
import traitsui.api as trui


class short_rate(trapi.HasTraits):
    name = trapi.Str
    rate = trapi.Float
    time_list = trapi.Array(dtype=np.float, shape=(1, 5))
    disc_list = trapi.Array(dtype=np.float, shape=(1, 5))
    update = trapi.Button

    def _update_fired(self):
            self.disc_list = np.exp(-self.rate * self.time_list)

v = trui.View(trui.Group(trui.Item(name='name'),
                         trui.Item(name='rate'),
                         trui.Item(name='time_list', label='Insert Time List Here'),
                         trui.Item('update', show_label=False),
                         trui.Item(name='disc_list', label='Press Update for Factors'),
                         show_border=True, label='Calculate Discount Factors'),
              buttons=[trui.OKButton, trui.CancelButton],
              resizable=True)

sr = short_rate()
sr.configure_traits(view=v)

