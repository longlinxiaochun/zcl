# -*- coding: utf-8 -*-
# simulation:Geometric Brownian Motion
import pandas as pd


def sn_random_numbers(shape, antithetic=True, moment_matching=True,
                      fixed_seed=False):
    """Returns an array of shape shape with (pesudo)random numbers
    that are standard normally distributed

    Parameters
    ==========
    shape : tuple(o,n,m)
        generation of array with shape(o,n,m)
    antithetic : Boolean
        generation of antithetic variates
    moment_matching : Boolean
        matching of first and secondmoments
    fixed_seed :  Boolean
        flag to fix the seed

    Return
    =======
    ran : (o,n,m) array of (pseudo)random numbers
    """
    if fixed_seed:
        np.random.seed(1000)
    if antithetic:
        ran = np.random.standard_normal((shape[0], shape[1], shape[2] / 2))
    else:
        ran = np.random.standard_normal(shape)
    if moment_matching:
        ran -= np.mean(ran)
        ran /= np.std(ran)
    if shape[0] == 1:
        return ran[0]
    else:
        return ran


class simulation_class(object):
    """Providing base methods for simulation classes

    Attributes
    ==========
    name : string
        name of the object
    mar_env :instance if market_environment
        market environment data for simulation
    corr : Boolean
        True if correlated with other model

    Methods
    =======
    generate_time_grid::
        returns time grid for simulation
    get_instrument_values :
    returns the current instrument value
    """

    def __init__(self, name, mar_env, corr):
        try:
            self.name = name
            self.pricing_date = mar_env.pricing_date
            self.initial_value = mar_env.get_constant('initial_value')
            self.volatility = mar_env.get_constant('volatility')
            self.final_date = mar_env.get_constant('final_date')
            self.currency = mar_env.get_constant('currency')
            self.frequency = mar_env.get_constant('frequency')
            self.paths = mar_env.get_constant('paths')
            self.discount_curve = mar_env.get_curve('discount_curve')
            try:
                self.time_grid = mar_env.get_list('time_grid')
            except:
                self.time_grid = None
            try:
                # if there are special dates, then add these
                self.special_dates = mar_env.get_list('special_dates')
            except:
                self.special_dates = []
            self.instrument_values = None
            self.correlated = corr
            if corr is True:
                # only needed in a portfolio context when
                # risk factors are correlated
                self.cholesky_matrix = mar_env.get_list('cholesky_matrix')
                self.rn_set = mar_env.get_list('rn_set')[self.name]
                self.random_numbers = mar_env.get_list('random_numbers')
        except:
            print("Error parsing market environment")

    def generate_time_grid(self):
        start = self.pricing_date
        end = self.final_date
        time_grid = pd.date_range(start=start, end=end,
                                  freq=self.frequency).to_pydatetime()
        time_grid = list(time_grid)
        if start not in time_grid:
            time_grid.insert(0, start)
        if end not in time_grid:
            time_grid.append(end)
        if len(self.special_dates) > 0:
            time_grid.extend(self.special_dates)
            time_grid = list(set(time_grid))
            time_grid.sort()
        self.time_grid = np.array(time_grid)

    def get_instrument_values(self, fixed_seed=True):
        if self.instrument_values is None:
            self.generate_paths(fixed_seed=fixed_seed, day_count=365.)
        elif fixed_seed is False:
            self.generate_paths(fixed_seed=fixed_seed, day_count=365.)
        return self.instrument_values


class geometric_brownian_motion(simulation_class):
    """Class to generate simulated paths based on
    the Black-Scholes-Merton geometric Brownian motion model

    Attributes
    ==========
    name : string
        name of the object
    mar_env : instance of market_environment
        market environment data for simulation
    corr : Boolean
        True if correlated with other model simulation object

    Methods
    =======
    update :
        updates parameters
    generate_paths :
        returns Monte Carlo paths given the market environment
    """

    def __init__(self, name, mar_env, corr=False):
        super(geometric_brownian_motion, self).__init__(name, mar_env, corr)

    def update(self, initial_value=None, volatility=None, final_date=None):
        if initial_value is not None:
            self.initial_value = initial_value
        if volatility is not None:
            self.volatility = volatility
        if final_date is not None:
            self.final_date = final_date
        self.instrument_values = None

    def generate_paths(self, fixed_seed=False, day_count=365.):
        if self.time_grid is None:
            self.generate_time_grid()
        M = len(self.time_grid)
        I = self.paths
        paths = np.zeros((M, I))
        paths[0] = self.initial_value
        if not self.correlated:
            rand = sn_random_numbers((1, M, I), antithetic=False,
                                     fixed_seed=fixed_seed)  # 选择了对偶，则只生成了5000个数据无法计算
        else:
            # use random number object as provided in market environments
            rand = self.random_numbers
        short_rate = self.discount_curve.short_rate
        for t in range(1, len(self.time_grid)):
            # select the right time slice from te relevant random number set
            if not self.correlated:
                ran = rand[t]
            else:
                ran = np.dot(self.cholesky_matrix, rand[:, t, :])
                ran = ran[self.rn_set]
            dt = (self.time_grid[t] - self.time_grid[t-1]).days / day_count
            paths[t] = paths[t - 1] * np.exp((short_rate - 0.5 * self.volatility ** 2) * dt
                                             + self.volatility * np.sqrt(dt) * ran)
        self.instrument_values = paths


if __name__ == '__main__':
    """
    A usa case
    """
    from dx import *
    import datetime as dt
    import matplotlib.pyplot as plt
    me_gbm = market_environment('me_gbm', dt.datetime(2015, 1, 1))
    me_gbm.add_constant('initial_value', 36.)
    me_gbm.add_constant('volatility', 0.2)
    me_gbm.add_constant("final_date", dt.datetime(2015, 12, 31))
    me_gbm.add_constant('currency', 'EUR')
    me_gbm.add_constant('frequency', 'M')
    me_gbm.add_constant('paths', 10000)
    csr = constant_short_rate('csr', 0.05)
    me_gbm.add_curve('discount_curve', csr)
    gbm = geometric_brownian_motion('gbm', me_gbm)
    gbm.generate_time_grid()
    paths_1 = gbm.get_instrument_values()
    gbm.update(volatility=0.5)
    paths_2 = gbm.get_instrument_values()
    plt.figure(figsize=(8, 4))
    p1 = plt.plot(gbm.time_grid, paths_1[:, :10], 'b')
    p2 = plt.plot(gbm.time_grid, paths_2[:, :10], 'r-.')
    plt.grid(True)
    l1 = plt.legend([p1[0], p2[0]],
                    ['low volatility', 'high volatility'], loc=2)
    plt.gca().add_artist(l1)
    plt.xticks(rotation=30)
    plt.show()

