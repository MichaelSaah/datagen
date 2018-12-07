from .utilities import WeightedSampler

class suffix(WeightedSampler): # male only
    values = ['Jr.', 'Jr', 'Sr', 'Sr.', 'II', 'III', 'IV']
    weights = [0.2, 0.2, 0.2, 0.2, 0.066666666, 0.066666666, 0.066666666]
