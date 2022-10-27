#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import math

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

        self.laske_kesto()
        self.laske_koordinaatit()
        self.laske_nopeus()

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
        try:
            print(self.t_max)
            self.t = np.linspace(0, self.t_max, int(self.t_max / 0.01))
            self.x = 1/2 * 9.81 * self.t**2 * (np.sin(self.maki.theta) - self.pulkka.mu * np.cos(self.maki.theta))
            self.x_max = self.x[-1]
        except AttributeError:
            print('Kiihtyvän liikkeen kestoa ei ole määritetty.')

    def laske_nopeus(self):
        try:
            dt = self.t[1] - self.t[0]
            self.v = np.gradient(self.x, dt)
            self.v_max = self.v[-1]
        except AttributeError:
            print('Kiihtyvän pulkan paikka tai ajanhetket ei tiedossa.')

class PulkanHidastuvuus():
    def __init__(self, pulkka : Pulkka, kiihtyva_pulkka : PulkanKiihtyvyys):
        self.pulkka = pulkka
        self.v_0 = kiihtyva_pulkka.v_max
        self.x_0 = kiihtyva_pulkka.x_max
        
        self.laske_kesto()
        self.laske_koordinaatit()
        self.laske_nopeus()

    def laske_kesto(self):
        self.t_max =  self.v_0 / (self.pulkka.mu * 9.81)

    def laske_koordinaatit(self):
        """
        Laskee ja palauttaa hidastuvan liikkeen keston ja paikan alkaen hetkestä, jolloin hidastuva liike alkaa.

        Huom! Tässä käytetty t alkaa hetkestä 0.01 (sämpläys 0.01 s välein), koska kiihtyvä liike loppuu muuten
        samaan hetkeen. Tästä aiheutuu ongelmia nopeuden laskennassa.
        """
        self.t = np.linspace(0.01, self.t_max, int((self.t_max - 0.01) / 0.01)) # Huom. aika, eri kuin kiihtyvän loppuaika
        self.x = self.x_0 + self.v_0 * self.t - 1/2 * self.pulkka.mu * 9.81 * self.t**2

    def laske_nopeus(self):
        try:
            dt = self.t[1] - self.t[0]
            self.v = np.gradient(self.x, dt)
            self.v_max = self.v[-1]
        except AttributeError:
            print('Hidastuvan pulkan paikka tai ajanhetket ei tiedossa.')

class PulkkaSimulaatio():
    def __init__(self):
        mu_0 = 0.12 # lepokitka, puu-lumi
        mu = 0.06 # liikekitka, puu-lumi
        m = 25 # massa (kg)
        theta = 25 # mäen kaltevuus (rad)
        h = 10 # mäen korkeus (m)

        self.maki = Maki(theta, h)
        self.pulkka = Pulkka(mu, mu_0, m)

        # Konstruktoreissa lasketaan tarvittava data
        self.kiihtyva_pulkka = PulkanKiihtyvyys(self.pulkka, self.maki)
        self.hidastuva_pulkka = PulkanHidastuvuus(self.pulkka, self.kiihtyva_pulkka)

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

    def yhdista_vaiheet(self):
        """
        Tällä funktiolla yhdistetään kiihtyvän ja hidastuvan liikkeen vaiheet.
        """
        self.t = np.append(self.kiihtyva_pulkka.t, self.kiihtyva_pulkka.t_max + self.hidastuva_pulkka.t)
        self.x = np.append(self.kiihtyva_pulkka.x, self.hidastuva_pulkka.x)
        self.v = np.append(self.kiihtyva_pulkka.v, self.hidastuva_pulkka.v)

    def start(self):
        lahto = PulkanLahto(self.pulkka, self.maki)
        if lahto.onnistuu():
            self.yhdista_vaiheet()
            print('Lähtö onnistui')
            fig, axs = plt.subplots(2, 1)
            fig.subplots_adjust(hspace=0.5)

            axs[0].plot(self.t, self.x)
            axs[0].set_xlabel('t (s)')
            axs[0].set_ylabel('x (m)')
            axs[0].grid(True)

            axs[1].plot(self.t, self.v)
            axs[1].set_xlabel('t (s)')
            axs[1].set_ylabel('v (m/s)')
            axs[1].grid(True)

            plt.show()
        else:
            print('Lähtö ei onnistunut')


if __name__ == '__main__':
    pulkkasimulaatio = PulkkaSimulaatio()
    print(pulkkasimulaatio)
    pulkkasimulaatio.start()
