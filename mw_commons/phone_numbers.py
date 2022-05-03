'''Parse, validate, and format Malawian phone numbers'''

from collections import namedtuple
from typing import Tuple

import re

MALAWIAN_PHONE_NUMBERS_REGEXEN = [
    # Can't combine regexes into single regex because repeating capture
    # groups are not allowed by the standard re library
    r'^(\+?265|0)(?P<operator>88|9[89]|31)(?P<digits>\d{7})',
    r'^(?P<operator>1|212)(?P<digits>\d{6})$'
]

Carrier = namedtuple('Carrier', ('short_name', 'full_name'))

MTL = Carrier('MTL', 'Malawi Telecommunications Limited')
TNM = Carrier('TNM', 'Telekom Networks Malawi')
AIRTEL = Carrier('AIRTEL', 'Airtel Malawi')
ACCESS = Carrier('ACL', 'Access Communications Limited')

def is_valid_phone_number(phone_number : str) -> bool:
    '''Checks if given phone number is a valid Malawian phone number
    
    >>> is_valid_phone_number('+265-888-800-900')
    True
    >>> is_valid_phone_number('0888800900')
    True
    >>> is_valid_phone_number('088880090') # Missing one digit
    False
    >>> is_valid_phone_number('+250-790-801-197')
    False
    '''
    return PhoneNumber._parse_phone_number(phone_number) is not None

class PhoneNumber:
    '''Parsed phone number'''
    
    def __init__(self, source : str) -> None:
        match = self._parse_phone_number(source)      
        if not match:
            raise ValueError(f'Invalid phone number: {source}')

        self.operator_id = match['operator']
        self.digits = match['digits']
    
    def to_internationalized(self, humanize=False) -> str:
        '''Returns phone number as string with +265 prefix
        
        >>> phone_number = PhoneNumber('0888800900')
        >>> phone_number.to_internationalized()
        '265888800900'
        >>> phone_number.to_internationalized(humanize=True)
        '+265-88-880-0900'
        '''
        if not humanize:
            return f'265{self.operator_id}{self.digits}'
            
        return f'+265-{self.operator_id}-{self._get_formatted_digits()}' 
        
    def to_localized(self, humanize=False) -> str:
        '''Returns phone number as string with 0 prefix

        >>> phone_number = PhoneNumber('+265888800900')
        >>> phone_number.to_localized()
        '0888800900'
        >>> phone_number.to_localized(humanize=True)
        '088-880-0900'
        '''
        if not humanize:
            return f'0{self.operator_id}{self.digits}'
        
        return f'0{self.operator_id}-{self._get_formatted_digits()}'
    
    def get_carrier(self) -> Tuple[str, str]:
        '''Returns carrier information for the phone number
        
        >>> phone_number = PhoneNumber('+265-888-800-900')
        >>> carrier = phone_number.get_carrier()
        >>> carrier.short_name
        'TNM'
        >>> carrier.full_name
        'Telekom Networks Malawi'
        '''
        match self.operator_id:
            case '1':
                return MTL
            case '88'|'31':
                return TNM
            case '98'|'99':
                return AIRTEL
            case '212':
                return ACCESS
            case _:
                raise ValueError(f'Invalid Mobile Carrier identifier {self.operator_id}')
    
    @staticmethod
    def _parse_phone_number(source : str) -> re.Match:
        for regex in MALAWIAN_PHONE_NUMBERS_REGEXEN:
            match = re.match(regex, re.sub(r'(-|\s+)', '', source))
            
            if match:
                return match
        else:
            return None
             
    def _get_formatted_digits(self):
        digit_groups = []
        digits = self.digits

        while len(digits) / 3 > 2:
            digit_groups.append(digits[:3])
            digits = digits[3:]
            
        digit_groups.append(digits) # Add trailing digits

        return '-'.join(digit_groups)

if __name__ == '__main__':
    import doctest

    doctest.testmod()