import numpy as np
import matplotlib.pyplot as plt


def wiener(n, mu=0, sig=1, rng=None):
# would be dangerous to expose without a timeout,
# could easily block with large sigma and small range
    s = np.zeros(n)

    for i in range(1, n):
        step = s[i-1] + np.random.normal(mu, sig)
        if rng:
            while step > mu + rng/2 or step < mu - rng/2:
                step = s[i-1] + np.random.normal(mu, sig)
        s[i] = step    

    return s


plt.plot(wiener(1000))
    
plt.show()
