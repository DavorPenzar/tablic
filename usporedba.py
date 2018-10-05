#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
Skripta za testiranje igraca igre tablic.

"""

import random
import six
import sys
import time

from engine import Tablic
from pohlepni_log import PohlepniLog
from minimax_log import MinimaxLog
from pohlepni_igrac import PohlepniIgrac
from minimax_igrac import MinimaxIgrac
from io_igrac import IOIgrac
from promatrac_log import PromatracLog

# Broj partija za testiranje.
N = 1

# Rezultat ce se ispisivati nakon svake k-te partije.  Ipak, ispisuje se i
# rezultat nakon 1. partije da se odmah vidi okvirno vrijeme potrebno za
# igranje jedne partije.
k = 1

# Detalji o nerjesenim partijama ispisuju se ako je ispisNerjesenih True.
ispisNerjesenih = False

# Igraci koji ce se testirati.  Redoslijed igraca zadaje redoslijed kojim ce
# biti na potezu u partijama.  Svaki igrac reprezentiran je rjecnikom s
# kljucevima 'klasa', 'args', 'kwargs', a dodaju se u igru pozivom
#     >>> igra.dodajIgraca(igrac['klasa'], *igrac['args'], **igrac['kwargs'])
igraci = ({'klasa' : MinimaxIgrac, 'args' : tuple(), 'kwargs' : {'ime' : 'Marconi', 'maxDubina' : 3, 'maxT' : 15.0}},
          {'klasa' : IOIgrac, 'args' : tuple(), 'kwargs' : {'ime' : 'Popeye'}})

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

# Ako je pri pokretanju skripte zadan argument "-r", redoslijed igraca u tuple-u igraci se obrce.  Ako je zadan argument "-p", redoslijed igraca permutira
# se slucajnim izborom.  Ostali dodatni argumenti se ne prepoznaju.
if len(sys.argv) == 2:
    if sys.argv[1] == '-r':
        igraci = tuple(reversed(igraci))
    elif sys.argv[1] == '-p':
        igraci = list(igraci)
        random.shuffle(igraci)
        igraci = tuple(igraci)
    else:
        raise RuntimeError("Dodatni argument `{0:s}' nije prepoznat.".format(sys.argv[1]))
elif len(sys.argv) != 1:
    raise RuntimeError("Skripta se pokrece s jednim argumentom `-r' (obrnuti redoslijed igraca) ili `-p' (slucajni redoslijed igraca), ili bez argumenata.")

# Ispis igraca redom kojim su na potezu.
print('Igraci redom po potezima:')
for i in range(len(igraci)):
    print("\t{0:d}.\t{1:s}({2:s})".format(i + 1,
                                          igraci[i]['klasa'].__name__,
                                          '{0:s}{2:s}{1:s}'.format(str.join(', ', [repr(x) for x in [i] + list(igraci[i]['args'])]),
                                                                   str.join(', ', ['{0:s} = {1:s}'.format(x, repr(y)) for x, y in six.iteritems(igraci[i]['kwargs'])]),
                                                                   ', ' if igraci[i]['kwargs'] else '')))

# U listi akumulirano spremljeni su akumulirani brojevi bodova igraca kroz
# partije, a u listi pobjede brojevi partija u kojima su pobjedili.  U listi
# nerjeseno spremljeni su parovi indeksa partije i tuple-a igraca koji su u tim
# partijama dijelili prvo mjesto.
akumulirano = [0 for i in range(len(igraci))]
pobjede = [0 for i in range(len(igraci))]
nerjeseno = list()

##  * * *  FORMAT ISPISA  * * *
##
##  Primjer testiranja 2 igraca.
##
##  N.
##  	t s (T s)
##  	igrac1 vs. igrac2
##  	[b1, b2]
##  	[B1, B2]
##  	[p1, p2]
##  	n
##  Nerjesene:
##  	(N1, (i11, i12))
##  	(N2, (i21, i22))
##
##  Legenda:
##      N   --  redni broj partije,
##      t   --  broj sekundi trajanja N-te partije,
##      T   --  ukupni broj sekundi od pocetka testiranja,
##      igrac1, igrac2  --  imena igraca redom kojim su na potezu,
##      b1, b2  --  broj ostvarenih bodova igraca igrac1, igrac2 u N-toj partiji,
##      B1, B2  --  akumulirani broj ostvarenih bodova igraca igrac1, igrac2 od
##                  pocetka testiranja,
##      p1, p2  --  broj pobjedenih partija igraca igrac1, igrac2 od pocetka
##                  testiranja
##      n   --  broj nerjesenih partija
##      N1, N2  --  redom redni brojevi nerjesenih partija
##      i11, i12    --  redni brojevi igraca koji su u N1-toj partiji imali
##                      najvise bodova (redni brojevi u smislu reda poteza,
##                      pocevsi s brojem 1),
##      i21, i22    --  analogno kao i11, i12, ali za N2-tu partiju.
##
##  Na samom kraju ispis je slican, ali bez informacija o konkretnoj partiji
##  (ispisano vrijeme odnosi se na cijelo testiranje, a od bodova su ispisani
##  samo akumulirani bodovi)
##
##  Moguce da se linije nakon linije "n" ne ce ispisivati (ako su od interesa,
##  donji kod se treba malo izmijeniti).
##


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
    if not (i and (i + 1) % k):
        print("\n{0:d}.".format(i + 1))
        print("\t{0:.3f} s ({1:.3f} s)".format(float(t1 - t0), float(t1 - t)))
        print("\t{0:s}".format(str.join(' vs. ', [igra.dohvatiIme(j) for j in range(igra.dohvatiBrojIgraca())])))
        print("\t{0:s}".format(repr(konacni_rezultat)))
        print("\t{0:s}".format(repr(akumulirano)))
        print("\t{0:s}".format(repr(pobjede)))
        print("\t{0:d}".format(len(nerjeseno)))
        if ispisNerjesenih and nerjeseno:
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
if ispisNerjesenih and nerjeseno:
    print("\tNerjesene:")
    for r in nerjeseno:
        print("\t\t{0:s}".format(repr(r)))
