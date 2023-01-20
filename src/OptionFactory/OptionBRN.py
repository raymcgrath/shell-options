from OptionFactory.OptionBase import OptionBase
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
from dateutil.relativedelta import relativedelta
import pandas as pd
from datetime import datetime

class OptionBRN(OptionBase):
    @property
    def expiry_date(self): 
        #BRN option expiry will be the last business day of the 2nd month before the delivery month. For example, BRN Jan-24 expiry date is 2023-11-30.
        busiday_us = pd.offsets.CustomBusinessDay(calendar=USFederalHolidayCalendar())
        prior_month_start_date = self.delivery_month_start_date() - relativedelta(months=1)
        expdate = (prior_month_start_date - busiday_us).to_pydatetime().date()
        return expdate