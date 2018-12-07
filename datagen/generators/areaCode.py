from .utilities import IntegerBetween

class areaCode:
    l = 100
    u = 999
    ib = IntegerBetween()
    def __call__(self):
        return str(self.ib(self.l, self.u))

