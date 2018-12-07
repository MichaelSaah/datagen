from .firstNameMale import firstNameMale
from .firstNameFemale import firstNameFemale
from .suffix import suffix
from .prefixMale import prefixMale
from .prefixFemale import prefixFemale
from .lastName import lastName
import random


class fullName:
    male_name = firstNameMale()
    female_name = firstNameFemale()
    suffix = suffix()
    prefix_male = prefixMale()
    prefix_female = prefixFemale()
    last_name = lastName()

    def __call__(self):
        if random.getrandbits(1):
            return self.prefix_male() + ' ' + self.male_name() + ' ' \
               + self.male_name() + ' ' + self.last_name()
        else:
            return self.prefix_female() + ' ' + self.female_name() + ' ' \
               + self.female_name() + ' ' + self.last_name()


