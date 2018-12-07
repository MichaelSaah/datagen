from .utilities import IntegerBetween

class internationalCode:
    l = 1
    u = 999
    ib = IntegerBetween()
    def __call__(self):
        return '+' + str(self.ib(self.l, self.u))

