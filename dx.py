# -*- coding: utf-8 -*-
# Valuation Framework
import numpy as np


def get_year_deltas(date_list, day_count=365.):
    """Return vector of floats with day deltas in years.
    Initial value normalized to zero.

    Parameters
    ==========
    date_list : list or array
        collection of datetime objects
    day_count : float
        number of days for a year

    Return
    ======
    delta_list : array
        year fractions
    """
    start = date_list[0]
    delta_list = [(date - start).days / day_count
                  for date in date_list]
    return np.array(delta_list)


class constant_short_rate(object):
    """Class for constant short rate discounting

    Attributes
    ==========
    name : string
        name of the object
    short_rate : float (positive)
        constant rate for discounting

    Methods
    =======
    get_discount_factors :
        get discount factors given a list/array of datetime object
        or year fractions
    """

    def __init__(self, name, short_rate):
        self.name = name
        self.short_rate = short_rate
        if short_rate < 0:
            raise ValueError('Short rate negative.')

    def get_discount_factors(self, date_list, dtobjects=True):
        if dtobjects is True:
            dlist = get_year_deltas(date_list)
        else:
            dlist = np.array(date_list)
        dflist = np.exp(self.short_rate * np.sort(-dlist))
        return np.array((date_list, dflist)).T


class market_environment(object):
    """Class to model a market environment relevant for valuation

    Attributes
    ==========
    name : string
    pricing_date : datetime object

    Methods
    =======
    add_constant:
        adds constant(e.g. model parameter)
    get_constant:
        gets a constant
    add_list:
        gets a list
    add_curve:
        adds a market curve (e.g. yield curve)
    get_curve:
        gets a market curve
    add_environment :
        adds and overwrites whole market envirtonments
        with constants, lists, and curves
    """

    def __init__(self, name, pricing_date):
        self.name = name
        self.pricing_date = pricing_date
        self.constants = {}
        self.lists = {}
        self.curves = {}

    def add_constant(self, key, constant):
        self.constants[key] = constant

    def get_constant(self, key):
        return self.constants[key]

    def add_list(self, key, list_object):
        self.lists[key] = list_object

    def get_list(self, key):
        return self.lists[key]

    def add_curve(self, key, curve):
        self.curves[key] = curve

    def get_curve(self, key):
        return self.curves[key]

    def add_environment(self, env):
        # overwrites existing values, if they exit
        for key in env.constants:
            self.constants[key] = env.constants[key]
        for key in env.lists:
            self.lists[key] = env.lists[key]
        for key in env.curves:
            self.curves[key] = env.curves[key]