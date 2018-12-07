from .utilities import Sampler, WeightedSampler

class streetName:
    names = Sampler(['Magnolia', 'Cherry', 'Chestnut', 'Jackson', 'Thomas', 'Montgomery', 'Pennsylvania', 'Washington', 'Willow', 'Beech', 'South', 'North', 'Sherman',
'Oregon', 'Ash', 'Spruce', 'Pine', 'Market', 'Main'])
    types = WeightedSampler(['St.', 'Ave.', 'Dr.', 'Rd.', 'Blvd.'],
                            [0.7, 0.05, 0.05, 0.15, 0.05])
    def __call__(self):
        return self.names() + ' ' + self.types()

