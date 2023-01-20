from typing import List
from fastapi import FastAPI
import datetime
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, validator
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from db_methods import * 
from schemas import *
import optionfunctions as optf

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/today")
async def test():
    return datetime.date.today()

@app.post("/submitvoldata")
async def submitvoldata(voldata: ContractVolDataList):
    submit_vol_data(voldata)    
    response = "Success"
    return response

@app.get("/getvoldata")
async def getvoldata():
    return get_vol_data()

@app.post("/priceoption")
async def price_option(optionparams: OptionCalcInput):
    price  = optf.price_option(optionparams)
    result = {"PRICE":price}
    return result

@app.get("/" , response_class=HTMLResponse)
async def root():
    today = datetime.date.today()
    year = today.strftime("%Y")
    #resp_string = "<html>WOPR™ ©Nice To See You, Thanks for stopping by ..... {year}<html>"
    html_content = """
    <html>
        <head>
            <title>OPTIONS CALCULATOR</title>
        </head>
        <body>        
            <hr>  
            <center>     
                <br><br><br><br>
                ────────────────────────────────<br>
                ────────▄███████████████▄───────<br>
                ───────███████████████████──────<br>
                ─────██████▀───██───▀███████────<br>
                ───████████────██────████████───<br>
                ──███───▀███───██───███▀───███──<br>
                ──████────██───██───██────████──<br>
                ─██████───██───██───██───██████─<br>
                ─██──██───██───██───██───██──██─<br>
                ─██───██───██──██──██───██───██─<br>
                ███───██───██──██──██───██───███<br>
                ███────██──██──██──██──██────███<br>
                ████───██──██──██──█───██───████<br>
                ██─██───██──█──██──█──██───██─██<br>
                ██──██──██──██─██─██──██──██──██<br>
                ██──███──██─██─██─██─██──███──██<br>
                ██───██──██──█─██─█──██──██───██<br>
                ██────██──██─█─██─█─██──██────██<br>
                ███▄───██──█─█─██─█─█───█───▄███<br>
                ████▄───██─█──█──█──█──█───▄████<br>
                ─█████───█──█─█──█─█──█───█████─<br>
                ───████───█──────────█───████───<br>
                ─────███────────────────███─────<br>
                ──────██────────────────██──────<br>
                ──────██────────────────██──────<br>
                ──────████████▄──▄████████──────<br>
                ──────████████████████████──────<br>
                ──────────────▀██▀──────────────<br>
                ────────────────────────────────<br>
                ──▄█████▄─██─────────────██─██──<br>
                ──██───▀▀─██─────────────██─██──<br>
                ──██▄─────██─────────────██─██──<br>
                ──██████▄─█████▄─▄█████▄─██─██──<br>
                ───▀█████─██──██─███──██─██─██──<br>
                ───────██─██──██─██████▀─██─██──<br>
                ──▄▄──▄██─██──██─███──▄▄─██─██──<br>
                ──▀█████▀─██──██─▀█████▀─██─██──<br>
                ────────────────────────────────<br>
                <br><br><br><br><br>
                    <h3><a style="font-family: Arial, Helvetica, sans-serif"href="docs">FASTApi Docs</a></h3>
                <br><br>
            </center>    
            <hr>
        </body>
    </html>
    """
    return html_content

#region for debug
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
#endregion