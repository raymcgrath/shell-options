from typing import List, Union
from pydantic import BaseModel
import datetime 

class OptionCalcInput(BaseModel):
    UNDERLYING: str
    EXPIRY: str
    INITIAL_PRICE: float
    STRIKE_PRICE: float
    PUT_CALL: str
    RISK_FREE_RATE: float
    IMPLIED_VOLATILITY: float
       
class OptionCalcInputList(BaseModel):
    calcdata: List[OptionCalcInput]     

class ContractVolData(BaseModel):
    contract_code: str
    datadate: datetime.date
    implied_vol: float    

class  ContractVolDataList(BaseModel):
    voldata: List[ContractVolData]