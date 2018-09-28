#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
Skripta za testiranje igraca igre tablic.

"""

import sys
import time

from engine import Tablic
from io_igrac import IOIgrac
from pohlepni_log import PohlepniLog
from minimax_log import MinimaxLog
from pohlepni_igrac import PohlepniIgrac
from minimax_igrac import MinimaxIgrac
from promatrac_log import PromatracLog

# Broj partija za testiranje.
N = 500

# Rezultat ce se ispisivati nakon svake k-te partije.
k = 25

# Igraci koji ce se testirati.  Redoslijed igraca zadaje redoslijed kojim ce
# biti na potezu u partijama.  Svaki igrac reprezentiran je rjecnikom s
# kljucevima 'klasa', 'args', 'kwargs', a dodaju se u igru pozivom
#     >>> igra.dodajIgraca(igrac['klasa'], *igrac['args'], **igrac['kwargs'])
igraci = ({'klasa' : MinimaxIgrac, 'args' : tuple(), 'kwargs' : {'ime' : 'Marconi', 'maxDubina' : 3, 'maxT' : 15.0}},
          {'klasa' : PohlepniIgrac, 'args' : tuple(), 'kwargs' : {'ime' : 'Popeye'}})

# Ako je pri pokretanju skripte zadan argument "-i", redoslijed igraca u tuple-u igraci se obrce.  Ostali
# dodatni argumenti se ne prepoznaju.
if len(sys.argv) == 2:
    if sys.argv[1] == '-i':
        igraci = tuple(reversed(igraci))
    else:
        raise RuntimeError("Dodatni argument `{0:s}' nije prepoznat.".format(sys.argv[1]))
elif len(sys.argv) != 1:
    raise RuntimeError("Skripta se pokrece s argumentom `-i' (obrnuti redoslijed igraca) ili bez argumenata.")

def deducirajPobjednika (konacni_rezultat):
    """
    Otkrij tko je skupio strogo najvise bodova.

    Argument funkcije mora biti povratna vrijednost funkcije
    Tablic.Log.konacniRezultat iz koje se trazi indeks igraca sa strogo
    najvecim brojem skupljenih bodova.  Ako vise igraca dijeli prvo mjesto,
    povratna vrijednost je uzlazno sortirani tuple njihovih indeksa.

    """

    pobjednik = [0]
    for i in range(1, len(konacni_rezultat)):
        if konacni_rezultat[i] == konacni_rezultat[pobjednik[0]]:
            pobjednik.append(i)
        elif konacni_rezultat[i] > konacni_rezultat[pobjednik[0]]:
            pobjednik = [i]

    if len(pobjednik) > 1:
        return tuple(pobjednik)

    return pobjednik[0]

# U listi akumulirano spremljeni su akumulirani brojevi bodova igraca kroz
# partije, a u listi pobjede brojevi partija u kojima su pobjedili.  U listi
# nerjeseno spremljeni su parovi indeksa partije i tuple-a igraca koji su u tim
# partijama dijelili prvo mjesto.
akumulirano = [0 for i in range(len(igraci))]
pobjede = [0 for i in range(len(igraci))]
nerjeseno = list()

# Pocetak ukupnog mjerenja vremena.
t = time.time()

# Igranje N partija.
for i in range(N):
    # Inicijalizacija igre.
    igra = Tablic()

    # Dodabvanje igraca u igru.
    for igrac in igraci:
        igra.dodajIgraca(igrac['klasa'], *igrac['args'], **igrac['kwargs'])

    # Pocetak mjerenja vremena partije.
    t0 = time.time()

    # Igranje partije.
    igra.igraj()

    # Kraj mjerenja vremena partije.
    t1 = time.time()

    # Racunanje konacnog rezultata i pribrajanje listama akumulirano, pobjede.
    rezultat = igra.dohvatiRezultat()
    konacni_rezultat = Tablic.Log.konacniRezultat(rezultat)
    for j in range(len(igraci)):
        akumulirano[j] += konacni_rezultat[j]
    pobjednik = deducirajPobjednika(konacni_rezultat)
    if isinstance(pobjednik, tuple):
        nerjeseno.append((i + 1, tuple(p + 1 for p in pobjednik)))
    else:
        pobjede[pobjednik] += 1

    # Eventualni ispis rezultata.
    if not (i + 1) % k:
        print('{0:d}.'.format(i + 1))
        print("\t{0:.3f} s ({1:.3f} s)".format(float(t1 - t0), float(t1 - t)))
        print("\t{0:s}".format(str.join(' vs. ', [igra.dohvatiIme(j) for j in range(igra.dohvatiBrojIgraca())])))
        print("\t{0:s}".format(repr(konacni_rezultat)))
        print("\t{0:s}".format(repr(akumulirano)))
        print("\t{0:s}".format(repr(pobjede)))
        print("\t{0:d}".format(len(nerjeseno)))
        if False and nerjeseno:
            print("\tNerjesene:")
            for r in nerjeseno:
                print("\t\t{0:s}".format(repr(r)))

# Kraj ukupnog mjerenja vremena.
t1 = time.time()

# Konacni ispis rezultata.
print("\nKonacno")
print("\t{0:.3f} s".format(float(t1 - t)))
print("\t{0:s}".format(repr(akumulirano)))
print("\t{0:s}".format(repr(pobjede)))
print("\t{0:d}".format(len(nerjeseno)))
if False and nerjeseno:
    print("\tNerjesene:")
    for r in nerjeseno:
        print("\t\t{0:s}".format(repr(r)))
