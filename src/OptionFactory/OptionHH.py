from OptionFactory.OptionBase import OptionBase
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
from dateutil.relativedelta import relativedelta
import pandas as pd

class OptionHH(OptionBase):
    @property
    def expiry_date(self):
        #HH option expiry is the last business day of the month before the delivery month. For example, HH Mar-24 expiry date is 2022-02-29. 
        #get a US holiday calendar *further definition of holidays is required. . 
        busiday_us = pd.offsets.CustomBusinessDay(calendar=USFederalHolidayCalendar())
        expdate = (self.delivery_month_start_date() - busiday_us).to_pydatetime().date()
        return expdate

