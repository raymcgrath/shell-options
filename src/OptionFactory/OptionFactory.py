from OptionFactory.OptionBRN import OptionBRN
from OptionFactory.OptionHH import OptionHH

class OptionFactory:
    @staticmethod
    async def create_option_object(option):
        underlying_code= option.UNDERLYING
        # underlying_code = option.get('underlying_code')
        if underlying_code =='BRN': 
            return await OptionBRN.create(option)
        elif underlying_code =='HH':            
            return await OptionHH.create(option)
        else: 
            raise ValueError(underlying_code)
            
