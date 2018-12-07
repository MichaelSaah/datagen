from .utilities import FloatBetween

class numberFloat:
# Note: floats are returned as floats, so they may have less than k digits after the decimal,
# for instance, 3.240 will be returned as 3.24. Document this.
    fb = FloatBetween()
    def __call__(self, l=-2**31, u=2**31, k=None):
        l = float(l)
        u = float(u)
        if k:
            k = int(k)
        return self.fb(l, u, k)
