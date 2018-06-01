# -*- coding:utf-8 -*-
# Benchmark case
import numpy as np
import scipy.stats as scs
import statsmodels.api as sm
import matplotlib as mpl
import matplotlib.pyplot as plt

np.random.seed(1000)


def gen_paths(S0, r, sigma, T, M, I):
    """Generates Monte Carlo paths for geometric Brownian motion

    :param S0: float
                initial stock/index value
    :param r: float
                constant short rate
    :param sigma: float
                constant volatility
    :param T: float
                final time horizon
    :param M: int
                number of time steps/intervals
    :param I: int
                number of paths to be simulated
    :return:
    paths : ndarray, shape(M + 1, I)
        simulated paths giventhe parameters
    """
    dt = float(T) / M
    paths = np.zeros((M + 1, I), np.float64)
    paths[0] = S0
    for t in range(1, M + 1):
        rand = np.random.standard_normal(I)
        rand = (rand - rand.mean()) / rand.std()
        paths[t] = paths[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt
                                         + sigma * np.sqrt(dt) * rand)
    return paths
S0 = 100
r = 0.05
sigma = 0.2
T = 1.0
M = 50
I = 250000
paths = gen_paths(S0, r, sigma, T, M, I)
"""
plt.plot(paths[:, :10])
plt.grid(True)
plt.xlabel('time steps')
plt.ylabel('index level')
"""
log_returns = np.log(paths[1:] / paths[0:-1])
plt.hist(log_returns.flatten(), bins=70, normed=True, label='frequency')
plt.grid(True)
plt.xlabel('log-return')
plt.ylabel('frequency')
x = np.linspace(plt.axis()[0], plt.axis()[1])
plt.plot(x, scs.norm.pdf(x, loc=r / M, scale=sigma / np.sqrt(M)),
         'r', lw=2, label='pdf')
plt.legend()
plt.show()
