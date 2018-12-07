from .streetNum import streetNum
from .streetName import streetName
from .zipCode import zipCode
from .cityName import cityName
from .stateCode import stateCode

class fullAddress:
    snum = streetNum()
    sname = streetName()
    zc = zipCode()
    cname = cityName()
    scode = stateCode()
    def __call__(self):
        return '{0} {1} {2}, {3} {4}'.format(self.snum(), self.sname(), self.cname(), self.scode(), self.zc())
