#!/usr/bin/env python3

from audioop import mul
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

def kiihtyvyyden_kesto(h, theta, mu):
    """
    Laskee kiihtyvän liikkeen keston laskukorkeuteen, -kulmaan ja kitkakertoimeen perustuen.
    """
    x = h / np.sin(theta)
    return np.sqrt((2*x) / (9.81 * (np.sin(theta) - mu * np.cos(theta))))

def kiihtyvan_pulkan_paikka():
    """
    Laskee ja palauttaa kiihtyvän liikkeen keston sekä paikkakoordinaatit.
    """
    t_max = kiihtyvyyden_kesto(pulkka_setup['h'], pulkka_setup['theta'], pulkka_setup['mu'])
    t = np.linspace(0, t_max, int(t_max / 0.01))
    theta = pulkka_setup['theta']
    mu = pulkka_setup['mu']
    return t, 1/2 * 9.81 * t**2 * (np.sin(theta) - mu * np.cos(theta))

def kiihtyvan_pulkan_nopeus():
    t, x = kiihtyvan_pulkan_paikka()
    return laske_nopeus(x, t)

def hidastuvan_liikkeen_kesto(v_0, mu):
    """
    Laskee ja palauttaa hidastuvan liikkeen keston alkaen hetkestä, jolloin hidastuva liike alkaa.
    """
    return v_0 / (mu * 9.81)

def hidastuvan_liikkeen_paikka(x_0, v_0, mu):
    """
    Laskee ja palauttaa hidastuvan liikkeen keston ja paikan alkaen hetkestä, jolloin hidastuva liike alkaa.

    Huom! Tässä käytetty t alkaa hetkestä 0.01 (sämpläys 0.01 s välein), koska kiihtyvä liike loppuu muuten
    samaan hetkeen. Tästä aiheutuu ongelmia nopeuden laskennassa.
    """
    t_max = hidastuvan_liikkeen_kesto(v_0, mu)
    t = np.linspace(0.01, t_max, int((t_max - 0.01) / 0.01)) # Huom. aika, eri kuin kiihtyvän loppuaika
    return t, x_0 + v_0 * t - 1/2 * mu * 9.81 * t**2

def laske_nopeus(x, t):
    dt = t[1] - t[0]
    return np.gradient(x, dt)


def plot():
    fig, axs = plt.subplots(2, 1)
    fig.subplots_adjust(hspace=0.5)

    # Kiihtyvä liike
    aika, paikka = kiihtyvan_pulkan_paikka()
    nopeus = kiihtyvan_pulkan_nopeus()

    # Hidastuva liike
    hidastuvan_liikkeen_alkunopeus = nopeus[-1]
    hidastuvan_liikkeen_alkupaikka = paikka[-1]

    hid_t, hid_p = hidastuvan_liikkeen_paikka(hidastuvan_liikkeen_alkupaikka, hidastuvan_liikkeen_alkunopeus, pulkka_setup['mu'])

    # Yhdistetään tiedot plottausta varten
    aika = np.append(aika, aika[-1] + hid_t)
    paikka = np.append(paikka, hid_p)

    nopeus = laske_nopeus(paikka, aika)

    axs[0].plot(aika, paikka)
    axs[0].set_xlabel('t (s)')
    axs[0].set_ylabel('x (m)')
    axs[0].grid(True)

    axs[1].plot(aika, nopeus)
    axs[1].set_xlabel('t (s)')
    axs[1].set_ylabel('v (m/s)')
    axs[1].grid(True)

    plt.show()

def run():
    print('Lasketaan pulkkamäkeä!')
    print_setup()
    if lahtee_liikkeelle():
        plot()

class Maki():
    def __init__(self, theta, h):
        """
        Ottaa argumentiksi kulman asteina ja korkeuden metreinä.
        """
        self.h = h
        self.theta = theta * math.pi / 180 # Tallennetaan kulma radiaaneina

    def jyrkkyys(self):
        """
        Palauttaa mäen kaltevuuden radiaaneina.
        """
        return self.theta

    def korkeus(self):
        """
        Palauttaa mäen korkeuden meterinä.
        """
        return self.h

class Pulkka():
    def __init__(self, mu, mu_0, m):
        self.mu = mu
        self.mu_0 = mu_0
        self.m = m

class PulkanLahto():
    def __init__(self, pulkka, maki):
        self.pulkka = pulkka
        self.maki = maki

    def onnistuu(self):
        return self.pulkka.mu_0 < np.tan(self.maki.theta)

class PulkanKiihtyvyys():
    def __init__(self, pulkka : Pulkka, maki : Maki):
        self.pulkka = pulkka
        self.maki = maki

    def laske_kesto(self):
        """
        Laskee kiihtyvän liikkeen keston laskukorkeuteen, -kulmaan ja kitkakertoimeen perustuen.
        """
        x = self.maki.h / np.sin(self.maki.theta)

        # Kiihtyvän liikkeen kesto tallennetaan muuttujaan t_max
        self.t_max = np.sqrt((2*x) / (9.81 * (np.sin(self.maki.theta) - self.pulkka.mu * np.cos(self.maki.theta))))

    def laske_koordinaatit(self):
        """
        Laskee kiihtyvän liikkeen ajat ja paikat niitä vastaaviin luokkamuuttujiin.
        """
        self.laske_kesto()
        try:
            print(self.t_max)
            self.t = np.linspace(0, self.t_max, int(self.t_max / 0.01))
            self.x = 1/2 * 9.81 * self.t**2 * (np.sin(self.maki.theta) - self.pulkka.mu * np.cos(self.maki.theta))
        except AttributeError:
            print('Kiihtyvän liikkeen kestoa ei ole määritetty.')

class PulkanHidastuvuus():
    def __init__(self):
        pass

    def laske_kesto(self):
        pass

    def laske_ajat(self):
        pass

    def laske_paikat(self):
        pass

class PulkkaSimulaatio():
    def __init__(self):
        mu_0 = 0.12 # lepokitka, puu-lumi
        mu = 0.06 # liikekitka, puu-lumi
        m = 25 # massa (kg)
        theta = 25 # mäen kaltevuus (rad)
        h = 10 # mäen korkeus (m)

        self.maki = Maki(theta, h)
        self.pulkka = Pulkka(mu, mu_0, m)

    def __str__(self):
        return (
            '\n--------------------------\n'
            f"Lähtökorkeus: {self.maki.h} m\n"
            f"Mäen kaltevuus: {self.maki.theta / math.pi * 180} deg\n"
            f"Lepokitka: {self.pulkka.mu_0}\n"
            f"Liukukitka: {self.pulkka.mu}\n"
            f"Pulkan massa: {self.pulkka.m} kg\n"
            '--------------------------\n'
        )

    def start(self):
        lahto = PulkanLahto(self.pulkka, self.maki)
        if lahto.onnistuu():
            print('Lähtö onnistui')
            kiihtyva_vaihe = PulkanKiihtyvyys(self.pulkka, self.maki)
            kiihtyva_vaihe.laske_koordinaatit()
            hidastuva_vaihe = PulkanHidastuvuus()
        else:
            print('Ei onnistunut')

    def kiihtyvyyden_kesto(self):
        """
        Laskee kiihtyvän liikkeen keston laskukorkeuteen, -kulmaan ja kitkakertoimeen perustuen.
        """
        x = self.h / np.sin(self.theta)
        self.kiihtyvan_liikkeen_kesto = np.sqrt((2*x) / (9.81 * (np.sin(self.theta) - self.mu * np.cos(self.theta))))

    def kiihtyvan_pulkan_paikka(self):
        """
        Laskee ja palauttaa kiihtyvän liikkeen keston sekä paikkakoordinaatit.
        """
        # t_max = kiihtyvyyden_kesto(pulkka_setup['h'], pulkka_setup['theta'], pulkka_setup['mu'])
        self.kiihtyvyyden_ajat = np.linspace(0, self.kiihtyvan_liikkeen_kesto, int(self.kiihtyvan_liikkeen_kesto / 0.01))
        self.kiihtyvyyden_paikat = 1/2 * 9.81 * self.kiihtyvyyden_ajat**2 * (np.sin(self.theta) - self.mu * np.cos(self.theta))


if __name__ == '__main__':
    # run()
    pulkkasimulaatio = PulkkaSimulaatio()
    print(pulkkasimulaatio)
    pulkkasimulaatio.start()
