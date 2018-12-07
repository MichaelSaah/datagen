from .utilities import Sampler
from .firstName import firstName

class eMail_domain(Sampler):
    values = ['hotmail.com', 'gmail.com', 'yahoo.com', 'comcast.net', 'verizon.net']

class eMail_number(Sampler):
    values = list(map(str, range(100,1000)))

class eMail:
    names = firstName()
    domains = eMail_domain()
    numbers = eMail_number()
    def __call__(self):
        return self.names() + self.numbers() + '@' + self.domains()
