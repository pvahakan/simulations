#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pygame

class Oscillator:
    def __init__(self, k: float, h: float, m: float, c=0):
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
        '''
        Coefficient from the solution of differential equation.
        '''
        return - self.c / (2 * self.m)

    def beta(self):
        '''
        Coefficient from the solution of differential equation.
        '''
        return np.sqrt(4 * self.m * self.k - self.c**2) / (2 * self.m)

    def position(self, t: float):
        '''
        Calculates oscillators position at time t.
        '''
        a = self.alpha()
        b = self.beta()
        return self.h * np.exp(a * t) * (np.cos(b * t) - a / b * np.sin(b * t))

if __name__ == '__main__':
    k = 20
    h = 0.07
    m = 0.055
    c = 0.0005

    t = np.linspace(0, 3, 300)

    damped_oscillator = Oscillator(k, h, m, c)
    harmonic_oscillator = Oscillator(k, h, m)

    xd = damped_oscillator.position(t)
    xh = harmonic_oscillator.position(t)

    pygame.init()
    width = 640
    height = 480

    r = 5
    t = 0
    x = width / 2
    y = height / 2 + 500 * harmonic_oscillator.position(t)

    xd = width / 2 + 200
    yd = height / 2 + 500 * damped_oscillator.position(t)

    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, 'red', (x, y), r)
        pygame.draw.circle(screen, 'blue', (xd, yd), r)

        y += 500 * harmonic_oscillator.position(t)
        yd += 500 * damped_oscillator.position(t)
        t += 1

        pygame.display.flip()
        clock.tick(40)
    
    # plt.plot(t, xd)
    # plt.plot(t, xh)
    # plt.show()