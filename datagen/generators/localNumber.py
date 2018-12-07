from .utilities import IntegerBetween

class localNumber:
    l = 1000000000
    u = 9999999999
    ib = IntegerBetween()
    def __call__(self):
        return str(self.ib(self.l, self.u))
