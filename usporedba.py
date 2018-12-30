#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
Skripta za testiranje igraca igre tablic.

"""

import math
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
N = 50

# Rezultat ce se ispisivati nakon svake k-te partije.  Ipak, ispisuje se i
# rezultat nakon 1. partije (osim ako ona nije zadnja) da se odmah vidi okvirno
# vrijeme potrebno za igranje jedne partije, a rezultat zadnje partije se ne
# ispisuje.
k = 5

# Detalji o nerjesenim partijama ispisuju se ako je ispisNerjesenih True.
ispisNerjesenih = False

# Igraci koji ce se testirati.  Redoslijed igraca zadaje redoslijed kojim ce
# biti na potezu u partijama.  Svaki igrac reprezentiran je rjecnikom s
# kljucevima 'klasa', 'args', 'kwargs', a dodaju se u igru pozivom
#     >>> igra.dodajIgraca(igrac['klasa'], *igrac['args'], **igrac['kwargs'])
igraci = ({'klasa' : MinimaxIgrac, 'args' : tuple(), 'kwargs' : {'ime' : 'Marconi', 'maxDubina' : 3, 'maxT' : 15.0}},
          {'klasa' : PohlepniIgrac, 'args' : tuple(), 'kwargs' : {'ime' : 'Popeye'}})

def izraziVrijeme (t, preciznost = 2, predznak = False):
    """
    Dohvati string vremena t (u sekundama) izrazenog u potrebnim jedinicama.

    Povratna vrijednost je string oblika "[predznak][[[Dd ]Hh ]Mm ]Ss", gdje
    su:
        --  D   --  broj dana (iz intervala [1, +beskonacno)),
        --  H   --  broj sati (iz intervala [0, 24)),
        --  M   --  broj minuta (iz intervala [0, 60)),
        --  S   --  broj sekundi (iz intervala [0, 60)).
    Vodece nule se ne ispisuju (ako je, na primjer, t = 65, preciznost = 2 i
    predznak = False, povratni string je samo "1m 05.00s"), ali sekunde se
    uvijek ispisuju (cak i ako je t = 0).  Ako je predznak = True, predznak se
    nuzno ispisuje ispred vodece vrijednosti (ako je t < 0, predznak se ionako
    ispisuje).  Vrijednost preciznost zadaje broj decimalnih mjesta za ispis
    vrijednosti sekundi.

    """

    # Definiranje stringova za predznake.
    minus = '-'
    plus = '+'

    # Definiranje stringova za oznake mjernih jedinica vremena.
    dan = 'd'
    sat = 'h'
    minuta = 'm'
    sekunda = 's'

    # Izrazavanje negativnog vremena.
    if t < 0.0:
        return '{0:s}{1:s}'.format(minus, izraziVrijeme(-t, preciznost, False))

    # Ako je veca mjerna jedinica vec ispisana (na primjer sat), manja se mora
    # ispisati iako iznosi 0 (na primjer minuta ako je sat vec ispisan).
    # Obavezno ispisivanje zadano je varijablom ispisuj.
    ispisuj = False

    # Inicijalizacija povratnog stringa.
    t_str = plus if predznak and t else ''

    # Ispis dana.
    if t >= 86400.0:
        t_str += '{0:d}{1:s} '.format(int(math.floor(t / 86400.0)), dan)
        t -= 86400.0 * math.floor(t / 86400.0)

    # Ispis sati.
    if ispisuj or t >= 3600.0:
        t_str += '{1:{0:s}d}{2:s} '.format('02' if ispisuj else '', int(math.floor(t / 3600.0)), sat)
        t -= 3600.0 * math.floor(t / 3600.0)

        ispisuj = True

    # Ispis minuta.
    if ispisuj or t >= 60.0:
        t_str += '{1:{0:s}d}{2:s} '.format('02' if ispisuj else '', int(math.floor(t / 60.0)), minuta)
        t -= 60.0 * math.floor(t / 60.0)

        ispisuj = True

    # Ispis sekundi.
    t_str += '{2:{1:s}.{0:d}f}{3:s}'.format(preciznost, ('0{0:d}'.format(preciznost + 3) if preciznost else '02') if ispisuj else '', t, sekunda)

    # Povrat izrazenog vremena.
    return t_str

def deducirajPobjednika (konacni_rezultat):
    """
    Otkrij tko je skupio strogo najvise bodova.

    Argument funkcije mora biti povratna vrijednost funkcije
    Tablic.Log.konacniRezultat iz koje se trazi indeks igraca sa strogo
    najvecim brojem skupljenih bodova.  Ako vise igraca dijeli prvo mjesto,
    povratna vrijednost je uzlazno sortirani tuple njihovih indeksa.

    """

    # Dedukcija igraca s najvise bodova.
    pobjednik = [0]
    for i in range(1, len(konacni_rezultat)):
        if konacni_rezultat[i] > konacni_rezultat[pobjednik[0]]:
            pobjednik = [i]
        elif konacni_rezultat[i] == konacni_rezultat[pobjednik[0]]:
            pobjednik.append(i)

    # Obradivanje slucaja da vise igraca ima najvise bodova.
    if len(pobjednik) > 1:
        return tuple(pobjednik)

    # Povrat indeksa igraca sa strogo najvecim brojem bodova.
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
igraci = list(igraci)
print('Igraci redom po potezima:')
for i in range(len(igraci)):
    igraci[i]['kwargs'].pop('i', None)
    print("\t{0:d}.\t{1:s}({2:s})".format(i + 1,
                                          igraci[i]['klasa'].__name__,
                                          '{0:s}{2:s}{1:s}'.format(str.join(', ', [repr(x) for x in [i] + list(igraci[i]['args'])]),
                                                                   str.join(', ', ['{0:s} = {1:s}'.format(x, repr(y)) for x, y in six.iteritems(igraci[i]['kwargs'])]),
                                                                   ', ' if igraci[i]['kwargs'] else '')))
igraci = tuple(igraci)

# Varijabla T "pamti" akumulirani broj sekundi trajanja partija.
T = 0.0

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
##  Partija r/N.
##  	t s (mt; T1 + T2 = T)
##  	igrac1 vs. igrac2
##  	[b1, b2]
##  	[B1, B2]
##  	[p1, p2]
##  	n
##  Nerjesene:
##  	(r1, (i11, i12))
##  	(r2, (i21, i22))
##  	...
##
##  Legenda:
##      r   --  redni broj partije,
##      N   --  ukupni broj partija,
##      t   --  broj sekundi trajanja r-te partije,
##      mt  --  prosjecno vrijeme trajanja prvih r partija,
##      T1  --  akumulirano vrijeme trajanja prvih r partija,
##      T2  --  pretpostavljeno akumulirano vrijeme preostalih partija
##              izracunato po fromuli (N - r) * mt,
##      T   --  pretpostavljeno akumulirano vrijeme svih partija izracunato po
##              formuli N * mt,
##      igrac1, igrac2  --  imena igraca redom kojim su na potezu,
##      b1, b2  --  broj ostvarenih bodova igraca igrac1, igrac2 u r-toj
##                  partiji,
##      B1, B2  --  akumulirani broj ostvarenih bodova igraca igrac1, igrac2 u
##                  prvih r partija,
##      p1, p2  --  broj pobjedenih partija igraca igrac1, igrac2 u prvih r
##                  partija,
##      n   --  broj nerjesenih partija od prvih r partija,
##      r1, r2  --  redom redni brojevi nerjesenih partija od prvih r partija,
##      i11, i12    --  redni brojevi igraca koji su u r1-toj partiji imali
##                      najvise bodova (redni brojevi u smislu reda poteza,
##                      pocevsi s brojem 1),
##      i21, i22    --  analogno kao i11, i12, ali za r2-tu partiju,
##      ... --  ako je n > 2, preostali su retci analogni prethodnim dvama
##              retcima, a odnose se redom na 3., 4. itd. nerjesenu partiju od
##              prvih r partija,
##
##  Ako je n = 0, redak "n" zadnji je u ispisu za tu partiju.  Inace je,
##  naravno, redaka ispod retka "Nerjesene:" ukupno n i odnose se redom na tih
##  n nerjesenih partija.
##
##  Na samom kraju ispis je slican, ali bez informacija o konkretnoj partiji
##  (ispis vremena je u obliku "mt; T" gdje je T akumulirano vrijeme trajanja
##  svih partija, a od bodova su ispisani samo akumulirani bodovi).  Rezultat
##  zadnje partije se ne ispisuje, nego se samo ispisuje konacno stanje.
##
##  Moguce je da se linije nakon linije "n" ne ce ispisivati cak i ako je n > 0
##  (ako su od interesa, varijabla ispisNerjesenih mora biti postavljena na
##  True).
##

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

    # Dodavanje trajanja partije varijabli T.
    T += float(t1 - t0)

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
    if not (i and (i + 1) % k or i + 1 == N):
        print("\nPartija {0:d}/{1:d}:".format(i + 1, N))
        print("\t{0:s} ({1:s}; {2:s} + {3:s} = {4:s})".format(izraziVrijeme(float(t1 - t0)), izraziVrijeme(T / (i + 1)), izraziVrijeme(T), izraziVrijeme((N - i - 1) * T / (i + 1)), izraziVrijeme(N * T / (i + 1))))
        print("\t{0:s}".format(str.join(' vs. ', [igra.dohvatiIme(j) for j in range(igra.dohvatiBrojIgraca())])))
        print("\t{0:s}".format(repr(konacni_rezultat)))
        print("\t{0:s}".format(repr(akumulirano)))
        print("\t{0:s}".format(repr(pobjede)))
        print("\t{0:d}".format(len(nerjeseno)))
        if ispisNerjesenih and nerjeseno:
            print("\tNerjesene:")
            for r in nerjeseno:
                print("\t\t{0:s}".format(repr(r)))

# Konacni ispis rezultata.
print("\nKonacno ({0:d} partija):".format(N))
print("\t{0:s}; {1:s}".format(izraziVrijeme(T / N), izraziVrijeme(T)))
print("\t{0:s}".format(repr(akumulirano)))
print("\t{0:s}".format(repr(pobjede)))
print("\t{0:d}".format(len(nerjeseno)))
if ispisNerjesenih and nerjeseno:
    print("\tNerjesene:")
    for r in nerjeseno:
        print("\t\t{0:s}".format(repr(r)))
