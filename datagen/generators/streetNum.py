from .utilities import IntegerBetween

class streetNum:
    ib = IntegerBetween()
    def __call__(self):
        return str(self.ib(1, 9999))

