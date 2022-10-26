#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import math

pulkka_setup = {
    'mu_0': 0.12, # lepokitka, puu-lumi
    'mu': 0.06, # liikekitka, puu-lumi
    'm': 25, # massa (kg)
    'h': 10, # lähtökorkeus (m)
    'theta': 25 * math.pi / 180 # mäen kaltevuus (rad)
}

t = np.linspace(0, 60, 180)

def print_setup():
    print('\n--------------------------')
    print(f"Lähtökorkeus: {pulkka_setup['h']} m")
    print(f"Mäen kaltevuus: {pulkka_setup['theta'] / math.pi * 180} deg")
    print(f"Lepokitka: {pulkka_setup['mu_0']}")
    print(f"Liukukitka: {pulkka_setup['mu']}")
    print(f"Pulkan massa: {pulkka_setup['m']} kg")
    print('--------------------------\n')

def lahtee_liikkeelle():
    return pulkka_setup['mu_0'] < np.tan(pulkka_setup['theta'])

def laske_paikka(t):
    """
    Laskee pulkan paikan mäen jyrkällä osalla ajanhetkellä t. Paikka 0 on lähtöpaikka
    ja paikan lukuarvo on metrejä lähtöpaikasta alamäkeen.
    """
    kulma = pulkka_setup['theta']
    paikat =  1/2 * 9.81 * t**2 * (np.sin(kulma) - pulkka_setup['mu'] * np.cos(kulma))
    maessa = paikat < pulkka_setup['h'] / np.sin(pulkka_setup['theta'])
    maen_alla = paikat > pulkka_setup['h'] / np.sin(pulkka_setup['theta'])
    pulkan_paikat = paikat[maessa]
    pulkan_paikat = np.append(pulkan_paikat, np.repeat(pulkan_paikat[-1], len(paikat[maen_alla])))
    print(len(paikat), len(paikat[maessa]), len(paikat[maen_alla]))
    print(pulkan_paikat)
    return pulkan_paikat

def laske_nopeus(x, t):
    dt = t[1] - t[0]
    return np.gradient(x, dt)


def plot():
    fig, axs = plt.subplots(2, 1)
    fig.subplots_adjust(hspace=0.5)

    paikka = laske_paikka(t)
    nopeus = laske_nopeus(paikka, t)

    axs[0].plot(t, paikka)
    axs[0].set_xlabel('t (s)')
    axs[0].set_ylabel('x (m)')

    axs[1].plot(t, nopeus)
    axs[1].set_xlabel('t (s)')
    axs[1].set_ylabel('v (m/s)')

    plt.show()

def run():
    print('Lasketaan pulkkamäkeä!')
    print_setup()
    if lahtee_liikkeelle():
        plot()

if __name__ == '__main__':
    run()