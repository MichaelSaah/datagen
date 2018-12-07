import time
from .utilities import time_formatter

class timeNow:
    tf = time_formatter()
    def __call__(self, format='%H:%M:%S'):
        return self.tf(format, int(time.time()))

