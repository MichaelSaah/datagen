from .utilities import IntegerBetween

class zipCode:
    ib = IntegerBetween()
    def __call__(self):
        num = self.ib(0, 99999)
        zc = str(num)
        while len(zc) < 5:
            zc = '0' + zc
        return zc

