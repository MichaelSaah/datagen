import random
from .firstNameMale import firstNameMale
from .firstNameFemale import firstNameFemale

class firstName:
    male_name = firstNameMale()
    female_name = firstNameFemale()

    def __call__(self):
        if random.getrandbits(1):
            return self.male_name()
        else:
            return self.female_name()
