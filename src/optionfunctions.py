from  OptionFactory.OptionFactory  import OptionFactory
from schemas import * 

async def price_option(optioninput: OptionCalcInput): 
    option = await OptionFactory.create_option_object(optioninput)  
    if optioninput.PUT_CALL.upper()=="PUT": 
        price = option.calc_put_value()
    else: 
        price = option.calc_call_value()
    return price