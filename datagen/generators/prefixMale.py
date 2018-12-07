from .utilities import WeightedSampler

class prefixMale(WeightedSampler):
    values = ['Dr.', 'Mr.', 'Sir']
    weights = [0.1, 0.85, 0.05]

