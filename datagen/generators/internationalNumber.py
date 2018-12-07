from .localNumber import localNumber
from .internationalCode import internationalCode

class internationalNumber:
    local = localNumber()
    code = internationalCode()
    def __call__(self):
        return code() + ' ' + local()

