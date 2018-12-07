from .utilities import time_formatter
import random, time

class timeRandom:
    tf = time_formatter()
    def __call__(self, format='%H:%M:%S'):
        rt = random.sample(range(-1262304000, int(time.time())), 1)[0] # start time is jan 1, 1930
        return self.tf(format, rt)
