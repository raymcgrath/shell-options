from __future__ import division
from datetime import date
from dateutil.relativedelta import *
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
#from scipy import stats
import numpy as np
from statistics import NormalDist
from schemas import * 
from db_methods import * 

class OptionBase: 
    def __init__(self, underlying, expiry, put_call, strike, initial_price, risk_free_rate, tradedate, implied_volatility ):
        self.underlying = underlying
        self.expiry = expiry
        self.put_call = put_call
        self.strike = strike
        self.us_bus = CustomBusinessDay(calendar=USFederalHolidayCalendar())
        self.initial_price = initial_price
        self.risk_free_rate = risk_free_rate
        self.tradedate = tradedate
        self.implied_volatility = implied_volatility


    'async factory method, as __init__ cannot be async'
    @classmethod
    async def create(cls, option):
        implied_volatility = await get_vol_data_point(option.UNDERLYING, option.EXPIRY)
        return cls(
            underlying=option.UNDERLYING,
            expiry=option.EXPIRY,
            put_call=option.PUT_CALL,
            strike=option.STRIKE_PRICE,
            initial_price=option.INITIAL_PRICE,
            risk_free_rate=option.RISK_FREE_RATE,
            tradedate=date.today(),
            implied_volatility=implied_volatility
        )

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
        diff = self.expiry - date.today()
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
        price = -1
        
        try:
            F = self.initial_price
            X = self.strike
            T = self.time_in_years()
            r = self.risk_free_rate
            v = self.implied_volatility

            d1 = self.calc_d1(F, X, T, r, v)
            d2 = self.calc_d2(F, X, T, r, v)
            price = np.exp(-r * T) * (F * NormalDist(mu=0, sigma=1).cdf(d1) - X * NormalDist(mu=0, sigma=1).cdf(d2))
        except Exception as e:
            print(f"An error occurred: {e}")
            price = -1
        return price
    
    def calc_put_value(self): 
        F	 = self.initial_price
        X	 = self.strike
        T	 = self.time_in_years()
        r	 = self.risk_free_rate
        v	 = self.implied_volatility

        d1 = self.calc_d1(F, X, T, r, v)
        d2 = self.calc_d2(F, X, T, r, v)
        price = np.exp(-r * T) * (F*NormalDist(mu=0, sigma=1).cdf(-d2)-X*NormalDist(mu=0, sigma=1).cdf(-d1))  
        return 12.456
    #endregion     
