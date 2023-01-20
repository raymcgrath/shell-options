from DB import DB
import pandas as pd
from schemas import *
from  sqlalchemy import  * # create_engine, MetaData, Table, Column, ForeignKey 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

def submit_vol_data(voldata: ContractVolData ):
    try:
        df = pd.DataFrame([model.dict() for model in voldata.voldata])
        db = DB()
        db.execute_batch(df, "md.volatility")
        return True
    except:
        return False
    
def get_vol_data_point(contract, datadate):
    db = DB()
    sql = "select implied_vol from md.volatility where contract_code='{}' and datadate ='{}' "
    sql = sql.format(contract, datadate)
    result = db.fetch_one(sql)
    result = float(result[0])
    return result

def as_dict(obj):
    data = obj.__dict__
    data.pop('_sa_instance_state')
    return data

def get_vol_point(contract_code, datadate):
    db = DB()

    # POSTGRES_URI = "postgresql://postgres:1EsIfsze2Ki1CPmD2qFM@shelltest.czfeljkgnxtd.eu-west-2.rds.amazonaws.com:5432/mktdata"      
    # engine = create_engine(POSTGRES_URI, pool_pre_ping=True)
    # Session = sessionmaker(engine)
    # session = Session()
    # m = MetaData(schema='md', bind=engine)
    # volatility  = Table('volatility', m, autoload = True)
    # val = session.query(volatility.c.implied_vol).filter(volatility.c.contract_code=="BRN", volatility.c.datadate=="2020-01-05" ).one()
    
    return 0

def get_vol_data():
    db = DB()
    sql = "select * from md.volatility"
    df = db.get_df_from_sql(db.connection, sql)
    df = df.reset_index(drop=True)
    df.set_index(['id'])
    json = df.to_json(orient='records', indent=2)
    return json
