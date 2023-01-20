from __future__ import division
from datetime import date
from dateutil.relativedelta import *
import json
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
import math
#from scipy import stats
import numpy as np
from statistics import NormalDist
from schemas import * 
from db_methods import * 

class OptionBase: 
    def __init__(self, option: OptionCalcInput ):
        self.underlying =  option.UNDERLYING
        self.expiry = option.EXPIRY
        self.put_call = option.PUT_CALL
        self.strike = option.STRIKE_PRICE
        self.us_bus = CustomBusinessDay(calendar=USFederalHolidayCalendar())
        self.initial_price = option.INITIAL_PRICE
        self.risk_free_rate = option.RISK_FREE_RATE
        self.tradedate = date.today()
        self.implied_volatility = get_vol_data_point(self.underlying,self.tradedate)

    #region props
    @property
    def underlying(self):
        return self._underlying
    
    @underlying.setter
    def underlying(self, value):
        self._underlying = value
    
    @property
    def expiry(self):
        return self._expiry
    
    @expiry.setter
    def expiry(self, value):
        self._expiry = value
    
    @property
    def put_call(self):
        return self._put_call
    
    @put_call.setter
    def put_call(self, value):
        self._put_call = value    
        
    @property
    def strike(self):
        return self._strike
    
    @strike.setter
    def strike(self, value):
        self._strike = value    
    
    @property
    def us_bus(self):
        return self._us_bus
    
    @us_bus.setter
    def us_bus(self, value):
        self._us_bus = value    

    @property
    def initial_price(self):
        return self._initial_price
    
    @initial_price.setter
    def initial_price(self, value):
        self._initial_price = value    

    @property
    def implied_volatility(self):
        return self._implied_volatility
    
    @implied_volatility.setter
    def implied_volatility(self, value):
        self._implied_volatility = value    

    @property
    def risk_free_rate(self):
        return self._risk_free_rate
    
    @risk_free_rate.setter
    def risk_free_rate(self, value):
        self._risk_free_rate = value    

    #endregion props
        
    #region date functions    
    def delivery_month_start_date(self):
        #'Mar24' will get read as 1st Mar 2024
        return datetime.datetime.strptime(self.expiry,'%b%y')
    
    def time_in_years(self):
        #reldelta = relativedelta(self.expiry_date, date.today())
        diff = self.expiry_date - date.today()
        yearfrac = diff.days/365.0
        return yearfrac
    #endregion datefunctions

    #region option calc
    def calc_d1(self, F, X, T, r, v): 
        return (np.log(F/X) + (np.power(v, 2)/2)*T) /(v*np.sqrt(T))
    
    def calc_d2(self, F, X, T, r, v):         
        d1  = self.calc_d1(F, X, T, r, v)
        return d1 - v*np.sqrt(T)
            
    def calc_call_value(self): 
        F	 = self.initial_price
        X	 = self.strike
        T	 = self.time_in_years()
        r	 = self.risk_free_rate
        v	 = self.implied_volatility

        d1 = self.calc_d1(F, X, T, r, v)
        d2 = self.calc_d2(F, X, T, r, v)
        return np.exp(-r * T) * (F*NormalDist(mu=0, sigma=1).cdf(d1)-X*NormalDist(mu=0, sigma=1).cdf(d2)) #  NormalDist just to get past problem with scipy install
    
    def calc_put_value(self): 
        F	 = self.initial_price
        X	 = self.strike
        T	 = self.time_in_years()
        r	 = self.risk_free_rate
        v	 = self.implied_volatility

        d1 = self.calc_d1(F, X, T, r, v)
        d2 = self.calc_d2(F, X, T, r, v)
        return np.exp(-r * T) * (F*NormalDist(mu=0, sigma=1).cdf(-d2)-X*NormalDist(mu=0, sigma=1).cdf(-d1))   
    #endregion     
