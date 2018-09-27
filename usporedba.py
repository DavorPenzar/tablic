"""
Skripta za testiranje igraca igre tablic.

"""

import time

from engine import Tablic
from pohlepni_log import PohlepniLog
from minimax_log import MinimaxLog
from pohlepni_igrac import PohlepniIgrac
from minimax_igrac import MinimaxIgrac

# Broj partija za testiranje.
N = 10

# Rezultat ce se ispisivati nakon svake k-te partije.
k = 1

# Igraci koji ce se testirati.  Redoslijed igraca zadaje redoslijed kojim ce
# biti na potezu u partijama.  Svaki igrac reprezentiran je rjecnikom s
# kljucevima 'klasa', 'args', 'kwargs', a dodaju se u igru pozivom
#     >>> igra.dodajIgraca(igrac['klasa'], *igrac['args'], **igrac['kwargs'])
igraci = ({'klasa' : MinimaxIgrac, 'args' : tuple(), 'kwargs' : {'ime' : 'Marconi', 'maxDubina' : 3, 'maxT' : 15.0}},
          {'klasa' : PohlepniIgrac, 'args' : tuple(), 'kwargs' : {'ime' : 'Popeye'}})

def konacniRezultat (rezultat):
    """
    Izracunaj konacni rezultat partije igre tablic.

    Povratna vrijednost funkcije Tablic.dohvatiRezultat rezultate predstavlja
    "razlomljeno", to jest posebno prikazuje broj skupljenih bodova skupljenim
    kartama, broj ostvarenih tabli i otkriva koji je igrac skupio strogo
    najvise karata.  Povratna vrijednost ove funkcije je lista jedinstvenih
    cjelobrojnih vrijednosti koje zbrajaju bodove koje su igraci skupili na
    pojedinom elementu igre.

    """

    return [r['skupljeno'] + r['table'] * Tablic.vrijednostTable() + int(r['max'][0]) * Tablic.vrijednostMax() for r in rezultat]

def deducirajPobjednika (konacni_rezultat):
    """
    Otkrij tko je skupio strogo najvise bodova.

    Argument funkcije mora biti povratna vrijednost funkcije konacniRezultat iz
    koje se trazi indeks igraca sa strogo najvecim brojem skupljenih bodova.
    Ako vise igraca dijeli prvo mjesto, povratna vrijednost je uzlazno
    sortirani tuple njihovih indeksa.

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
    konacni_rezultat = konacniRezultat(rezultat)
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
        if nerjeseno:
            print("\tNerjesene:")
            for r in nerjeseno:
                print("\t\t{0:s}".format(repr(r)))

# Kraj ukupnog mjerenja vremena.
t1 = time.time()

# Konacni ispis rezultata.
print("\nKonacno")
print("\t{0:.3f} s".format(float(t1 - t0)))
print("\t{0:s}".format(repr(akumulirano)))
print("\t{0:s}".format(repr(pobjede)))
if nerjeseno:
    print("\tNerjesene:")
    for r in nerjeseno:
        print("\t\t{0:s}".format(repr(r)))
