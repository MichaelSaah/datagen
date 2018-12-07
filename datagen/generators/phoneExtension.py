from .utilities import IntegerBetween

class phoneExtension:
    l = 10
    u = 9999
    ib = IntegerBetween()
    def __call__(self):
        return 'x' + str(self.ib(self.l, self.u))

