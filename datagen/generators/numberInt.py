from .utilities import IntegerBetween

class numberInt:
    ib = IntegerBetween()
    def __call__(self, l=-2**31, u=2**31):
        l = int(l)
        u = int(u)
        return self.ib(l, u)
