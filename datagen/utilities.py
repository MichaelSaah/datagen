import random, string

# Building blocks for generators - not exposed to API

class Sampler:
    def __init__(self, values=None):
        if values:
            self.values = values
        self.n = len(self.values)
    def __call__(self):
        return self.values[random.randrange(self.n)]


class VosesAlias:
    """
    Vose's Alias is a variation of the alias algorithm for sampling
    from an arbitrary given discrete probability distribution. To use,
    simply pass a list of values (of any type) you'd like sampled, 
    and a list of weights specifying the probability of sampling each 
    value.

    Given the nature of floating-point comparison, we leave it up 
    to the user to make sure that the weights defines a 
    probability distribution; that is, that they sums to one. The 
    algorithm can handle some amount of numerical noise, so don't 
    sweat this too hard.
    """
    def __init__(self, values=None, weights=None):
        # we allow weights and values to be set externally by inheriting class
        # check to make sure either passed or set prior
        if (not values and not hasattr(self, 'values')) or \
        (not weights and not hasattr(self, 'weights')):
            raise ValueError('Values and weights must be passed or set by inheriting class')

        # if passed set, else assume already set
        if values and weights:
            self.values = values
            self.weights = weights

        if len(self.values) != len(self.weights):
            raise ValueError('Values and weights lack parity. \
                Please pass the same number of values and weights.')

        self.n = len(self.weights)

        scaled_weights = list(map(lambda x: x*self.n, self.weights))
        small = []
        large = []

        alias = [0]*self.n
        prob = [0]*self.n

        for i,p in enumerate(scaled_weights):
            if p < 1:
                small.append(i)
            else:
                large.append(i)

        while large and small:
            l = small.pop(0)
            g = large.pop(0)
            prob[l] = scaled_weights[l]
            alias[l] = g
            scaled_weights[g] = scaled_weights[g] + scaled_weights[l] - 1
            if scaled_weights[g] < 1:
                small.append(g)
            else:
                large.append(g)

        while large:
            g = large.pop(0)
            prob[g] = 1
       
        while small: # large should be exhausted first, 
                     # this catches numerical error
            l = small.pop(0)
            prob[l] = 1

        self.alias = alias
        self.prob = prob

    def __call__(self):
        i = random.randrange(self.n)
        if random.random() < self.prob[i]:
            return self.values[i]
        else:
            return self.values[self.alias[i]]


class WeightedSampler(VosesAlias):
    pass  

class IntegerBetween:
    @staticmethod
    def __call__(l, u):
        if l > u:
            raise ValueError('The lower bound must be less than or equal to the upper bound')
        return random.randrange(l, u+1)


class FloatBetween:
    @staticmethod
    def __call__(l, u, k=None):
        width = u - l
        f =  random.random() * width + l
        if k:
            return round(f, k)
        else:
            return f


class RandomChar(Sampler):
    values = string.ascii_letters + string.digits

