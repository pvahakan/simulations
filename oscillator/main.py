#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

k = 20
h = 0.07
m = 0.055
c = 0.15
# c = [0.5, 1.0, 1.5, 2.0]

def alpha(c, m):
    return - c/(2*m)

def beta(c, m, k):
    return np.sqrt(4*m*k - c**2) / (2*m)

def position(h, c, m, k, t):
    a = alpha(c, m)
    b = beta(c, m, k)
    return h * np.exp(a*t) * (np.cos(b*t) - a/b * np.sin(b*t))

if __name__ == '__main__':
    t = np.linspace(0, 5, 200)
    x = position(h, c, m, k, t)

    plt.plot(t, x)
    plt.show()
