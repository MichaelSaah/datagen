from .utilities import RandomChar, IntegerBetween

class randomString:
    rc = RandomChar()
    ib = IntegerBetween()
    def __call__(self, n=None):
        if n is None:
            n = self.ib(10,100)
        else:
            n = int(n)
        rs = ''
        for _ in range(n):
            rs += self.rc()
        return rs

