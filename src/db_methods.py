
from DB import DB
import pandas as pd
from schemas import *
import json
from sqlalchemy import create_engine
import asyncio

def submit_vol_data(voldata: ContractVolData ):
    try:
        df = pd.DataFrame([model.dict() for model in voldata.voldata])
        db = DB()
        db.execute_batch(df, "md.volatility")
        return True
    except:
        return False

def submit_vol_data_points(voldata: ContractVolData):
    sqlt = "select md.upsert_volatility('{}','{}',{})"
    db = DB()
    try: 
        rows = [model.dict() for model in voldata.voldata]
        for row in rows:
            ul = row['underlying']
            dd = row['datadate'].strftime('%Y-%m-%d')
            iv = row['implied_vol']
            sql = sqlt.format(ul, dd, iv)
            db.execute_sql(sql)        
        return True
    except:
        return False

async def get_vol_data_point(contract, datadate):
    db = DB()
    sql = "select implied_vol from md.volatility where underlying='{}' and datadate ='{}' "
    sql = sql.format(contract, datadate)
    result = await db.fetch_one(sql)
    #check if result is None
    if result is not None:
        return float(result[0])
    else:
        return 0.2

async def get_vol_data():
    db = DB()
    sql = "select * from md.volatility"
    df = db.get_df_from_sql(db.connection, sql)    
    df = df.reset_index(drop=True)
    df.set_index(['id'])
    df['datadate'] =  df['datadate'].apply(lambda x: x.strftime('%Y-%m-%d'))
    j = df.to_json(orient='records', indent=2)
    return j

def get_vol_data2():
    POSTGRES_URI = "postgresql://postgres:1EsIfsze2Ki1CPmD2qFM@shelltest.czfeljkgnxtd.eu-west-2.rds.amazonaws.com:5432/mktdata"   
    engine = create_engine(POSTGRES_URI, pool_pre_ping=True)
    sql = "select * from md.volatility"
    df = pd.read_sql_query(sql, con=engine)
    df['datadate'] =  df['datadate'].apply(lambda x: x.strftime('%Y-%m-%d'))
    j = df.to_json(orient='records', indent=2)    
    return j

