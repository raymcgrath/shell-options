import pandas as pd
import panel as pn
from datetime import datetime, timedelta
import panel_test.ui_widget_data as ui_widget_data
from panel import HSpacer, Spacer
import requests
from bokeh.models.widgets.tables import NumberFormatter, BooleanFormatter
import json


#region option pricing calls
result = ""

def create_option_pricer_payload(underlying, expiry, initial_price, strike_price, put_call, risk_free_rate):
    print(f"expiry: {expiry} ")
    #expiry = datetime.strptime(expiry, "%Y-%m-%d")
    payload = {
        "UNDERLYING": f'{underlying}',
        "EXPIRY": f'{expiry}',
        "INITIAL_PRICE": initial_price,
        "STRIKE_PRICE": strike_price,
        "PUT_CALL": f'{put_call}',
        "RISK_FREE_RATE": risk_free_rate
    }
    return payload

def price_option(event):
    global result
    payload = create_option_pricer_payload(underlying.value, expiry.value, initial_price.value, strike_price.value, put_call.value, risk_free_rate.value)
    result1 = requests.post("http://localhost:8003//priceoption", json=payload)
    print(result1)
    result = result1.json()["PRICE"]
    #format result as a string with 5 decimal places
    result = f"{result:.5f}"
    print(result)   
#endregion option pricing calls

#region volatility upload calls

def create_volatility_payload(underlying, expiry, implied_volatility):
    payload = { "voldata": [{
        "underlying": f'{underlying}',
        "datadate": f'{expiry}',
        "implied_vol": implied_volatility
    }]}
    return payload

def submit_vol_data_points(event):
    global df_implied_volatilities
    voldata = create_volatility_payload(v_underlying.value, v_expiry.value, v_implied_volatility.value)
    result = requests.post("http://localhost:8003//submitvoldata", json=voldata)
    df_implied_volatilities = get_implied_volatilities()
    return result


pn.config.raw_css.append("""
.custom-padding {
    padding-left: 20px;
}
""")

pn.extension(design="bootstrap", sizing_mode="stretch_width")
pn.extension("tabulator")

expiry_dates = ui_widget_data.brent_crude_option_expiry_dates(2025, 2026)

#region Logo and Title
logo_path = './logo/Shell_logo.svg'
shell_logo = pn.pane.SVG(logo_path, width=300, height=150)

logo_policy  = pn.pane.HTML("""
   By <a rel="nofollow" class="external free" href="https://www.shell.com">https://www.shell.com</a>, <a href="//en.wikipedia.org/wiki/File:Shell_logo.svg" title="Fair use of copyrighted material in the context of Shell plc">Fair use</a>, <a href="https://en.wikipedia.org/w/index.php?curid=3940014">Link</a>                                           
""")
title = pn.pane.Markdown("""\

""")
c0 = pn.Column(shell_logo, title, width=400, css_classes=['custom-padding'])
r0  = pn.Row(c0)
#endregion Logo and Title

#region Option Pricer Widgets
option_pricer_title = pn.pane.Markdown("### Option Pricer")
underlying = pn.widgets.Select(name='Underlying:', value='BRN', options=['BRN', 'HH'])
expiry = pn.widgets.Select(name='Expiry:', options=expiry_dates)
initial_price = pn.widgets.FloatInput(name='Initial Price:', value=5.5, step=0.001, start=0, end=1000)
strike_price = pn.widgets.FloatInput(name='Strike Price:', value=5.5, step=1e-1, start=0, end=1000)
put_call = pn.widgets.Select(name='Put/Call:', value='CALL', options=['CALL', 'PUT'])
risk_free_rate = pn.widgets.FloatInput(name='Risk Free Rate:', value=0.05, step=1e-2, start=0, end=1)
# date_picker = pn.widgets.DatePicker(
#     name='Datetime Picker', value=expiry_dates[0], enabled_dates=expiry_dates
# )
op_spacer1 = pn.Spacer(height=30)
button1 = pn.widgets.Button(name="Price Option", icon="calculator", button_type="primary")
result = ""
button1.on_click(price_option)
def get_option_price(clicks):
    return f"### Option Price: {result}"

option_price = pn.bind(get_option_price, button1.param.clicks)
#option_price = pn.bind(lambda value: f" ### option Price: {opt_px}", underlying.param.value)
opt_px = 0
#endregion Option Pricer Widgets

#region Implied Volatility Capture Widgets
v_title = pn.pane.Markdown("### Volatility Data")
v_underlying = pn.widgets.Select(name='Underlying:', value='BRN', options=['BRN', 'HH'])
v_expiry = pn.widgets.Select(name='Expiry:', options=expiry_dates)
v_implied_volatility = pn.widgets.FloatInput(name='Implied Volatility:', value=0.5, step=0.001, start=0, end=1)
v_spacer1 = pn.Spacer(height=30)
v_submit_volatility = pn.widgets.Button(name="Submit Volatility", icon="camera-down", button_type="primary")
v_submit_volatility.on_click(submit_vol_data_points)
v_spacer = pn.Spacer(height=50)

def get_implied_volatilities():
    result = requests.get("http://localhost:8003//getvoldata")
    data_json  = result.json()
    data = json.loads(data_json)
    df = pd.DataFrame(data)
    #rename the column headers to have Capitalized first letter
    df.columns = [col.capitalize() for col in df.columns]
    return df

df_implied_volatilities = get_implied_volatilities()

bokeh_formatters = {
    'float': NumberFormatter(format='0.00000'),
    'bool': BooleanFormatter(),
}

imp_vols = pn.widgets.Tabulator(df_implied_volatilities,  formatters=bokeh_formatters, hidden_columns=['index']) 
#imp_vols  = pn.pane.DataFrame(df_implied_volatilities, name="Implied Volatilities", height=300, width=500)
c1 = pn.Column(v_title,v_underlying,v_expiry,v_implied_volatility,v_spacer1,v_submit_volatility, v_spacer, imp_vols, css_classes=['custom-padding'],width=520)
#endregion Implied Volatility Capture Widgets

c2 = pn.Column(option_pricer_title,underlying, expiry, initial_price, strike_price, put_call, risk_free_rate,op_spacer1, button1, op_spacer1,option_price,css_classes=['custom-padding'],width=400)
spc = pn.Spacer(width=150)
r1 = pn.Row(c2,spc, c1)
c = pn.Column(r0,r1).servable()

#when button is pressed, I want to get the values of the widgets and send them to the backend
#I will then use the values to price the option
#I will then display the price of the option
#I will also display the greeks of the option




    
 
 
#

#python function to create a list of Monthly Option Expiry Dates

