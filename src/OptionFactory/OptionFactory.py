from OptionFactory.OptionBRN import OptionBRN
from OptionFactory.OptionHH import OptionHH

class OptionFactory:
    @staticmethod
    def create_option_object(option):
        underlying_code= option.UNDERLYING
        # underlying_code = option.get('underlying_code')
        if underlying_code =='BRN': 
            return OptionBRN(option)
        elif underlying_code =='HH':            
            return OptionHH(option)
        else: 
            raise ValueError(underlying_code)
            
