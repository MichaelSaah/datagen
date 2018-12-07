from .prefixMale import prefixMale
from .prefixFemale import prefixFemale
import random

class prefix:
    male_pf = prefixMale()
    fem_pf = prefixFemale()

    def __call__(self):
        if random.getrandbits(1):
            return self.male_pf()
        else:
            return self.fem_pf()

