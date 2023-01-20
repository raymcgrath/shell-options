from DB import DB
import pandas as pd
from schemas import *

def submit_vol_data(voldata: ContractVolData ):
    try:
        df = pd.DataFrame([model.dict() for model in voldata.voldata])
        db = DB()
        db.execute_batch(df, "md.volatility")
        return True
    except:
        return False
    
def get_vol_data_point(contract, date):
    db = DB()
    sql = "select implied_vol from md.volatility where contract_code='BRN' and datadate ='20200105'"
    result = db.fetch_one(db.connection, sql)
    return result

def get_vol_data():
    db = DB()
    sql = "select * from md.volatility"
    df = db.get_df_from_sql(db.connection, sql)
    df = df.reset_index(drop=True)
    df.set_index(['id'])
    json = df.to_json(orient='records', indent=2)
    return json
