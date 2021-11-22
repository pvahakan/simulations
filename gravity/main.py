#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import math

# Data

sun = {
  'mass': 1.989E30 # kg
}

earth = {
  'a': 1, # semi-major in AU
  'e': 0.01673, # eccentricity
  'T': None, # Time at perihelion
  'i': 0, # Inclination
  'N': None, # Longitude of ascendic node
  'w': 102.93, # Longitude of perihelion in degrees
  'm': 3.039E-6 # planetary mass / solar mass
}


class Planet:
  # https://stjarnhimlen.se/comp/tutorial.html
  def __init__(self, a, e, T, i, N, w, m):
    self.a = a # Semi major
    self.e = e # Eccentricity
    self.T = T # Time at perihelion
    self.i = i # Inclination
    self.N = N # Longitude of ascendic node
    self.w = w # Longitude of perihelion in degrees
    self.m = m # planetary mass / solar mass
    self.q = self.a * (1 - self.e) # Perihelion
    self.Q = self.a * (1 + self.e) # Aphelion
    self.P = 365.256898326 * self.a**(1.5 / math.sqrt(1 + self.m))
    self.n = 360 / P # Daily motion in degrees


# Omia kötöstyksiä
def F(m1, m2, r):
  G = 6.67430E-11 # SI-units
  return G * (m1 * m2) / r**2

def v(M, r, t):
  G = 6.67430E-11 # SI-units
  return G * M / r**2 * t

def M(M0, t, T):
  return M0 + 360 * (t / T)

def E(M, e):
  E_init = M

  while True:
    E_improved = M + (180 / math.pi) * e * math.sin(E_init)
    print(E_init)
    print(E_improved)
    if abs(E_init - E_improved < 0.00001):
      break
    else:
      E_init = E_improved

  return E_improved

def r(a, e, E):
  return a * (1 - e * math.cos(E))

if __name__ == '__main__':
  M0 = math.pi
  a = 10
  e = 0.4
  T = 10
  print(E(M0, e))
  # r = 5
  # theta = np.linspace(0, 2*np.pi, 100)
  # t = np.linspace(0, 10, 100)
  # y = 2*t

  # vx = np.cos(v(sun['mass'], r, t))
  # vy = np.sin(v(sun['mass'], r, t))

  # plt.plot(t, vx)


  # # plt.plot(r*np.cos(theta), r*np.sin(theta))
  # plt.show()
