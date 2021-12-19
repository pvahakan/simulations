#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

class Oscillator:
    def __init__(self, k, h, m, c=0):
        '''
        k = spring constant
        h = height at start
        m = mass
        c = viscous damping coefficient
        '''
        self.k = k
        self.h = h
        self.m = m
        self.c = c

    def alpha(self):
        return - self.c / (2 * self.m)

    def beta(self):
        return np.sqrt(4 * self.m * self.k - self.c**2) / (2 * self.m)

    def position(self, t):
        a = self.alpha()
        b = self.beta()
        return self.h * np.exp(a * t) * (np.cos(b * t) - a / b * np.sin(b * t))

if __name__ == '__main__':
    k = 20
    h = 0.07
    m = 0.055
    c = 0.15

    t = np.linspace(0, 3, 300)

    damped_oscillator = Oscillator(k, h, m, c)
    x = damped_oscillator.position(t)
    
    plt.plot(t, x)
    plt.show()