from .utilities import WeightedSampler

class prefixFemale(WeightedSampler):
    values = ['Dr.', 'Mrs.', 'Ms.', 'Miss', 'Madam']
    weights = [0.1, 0.4, 0.4, 0.05, 0.05]

