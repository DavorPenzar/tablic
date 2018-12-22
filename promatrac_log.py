# -*- coding: utf-8 -*-

"""
Implementacija klase "zapisnika" igre tablic koji ispisuje tijek igre.

"""

import copy
import math

from engine import Tablic
from io_igrac import IOIgrac

class PromatracLog (Tablic.Log):
    """
    Klasa za "zapisnik" za ispis tijeka igre na stdout.

    Zapisnik tijek igre ispisuje na stdout slicno kao sto se tijek igre
    ispisuje pri igranju objekta klase IOIgrac, a takav zapis svakog poteza
    (objekt klase str) sprema se u zapisnik.

    """

    def __init__ (self, log = list()):
        """
        Inicijaliziraj objekt klase PromatracLog.

        """

        Tablic.Log.__init__(self, log)

        # Inicijaliziraj relevantne varijable.

        self.__k = None # broj karata u spilu
        self.__n = None # broj igraca

    def __copy__ (self):
        log = Tablic.Log.__copy__(self)

        log.__k = self.__k
        log.__n = self.__n

        return log

    def __deepcopy__ (self, memodict = dict()):
        log = Tablic.Log.__deepcopy__(self, memodict)

        log.__k = copy.deepcopy(self.__k, memodict)
        log.__n = copy.deepcopy(self.__n, memodict)

        return log

    def novaPartija (self, n, igraci):
        """
        Ispisi podatke o novoj partiji.

        Ispis je slican kao u funkciji IOIgrac.saznajBrojIgraca, ali nijedan
        igrac nije oznacen.

        """

        # Postavi pocetne vrijednosti relevantnih varijabli.
        self.__k = 52 - Tablic.inicijalniBrojKarata_stol()
        self.__n = n

        # Ispisi pocetak partije.
        print("Partija za {0:d} igraca:".format(self.__n))
        for i in range(self.__n):
            print("\t{0:d}.\t{1:s}".format(i + 1, igraci[i].dohvatiIme()))
        print("\n")

    def novoDijeljenje (self, k, stol):
        """
        Ispisi na stdout kako izgleda stol nakon novog dijeljenja.

        """

        # Izracunaj ukupni broj dijeljenja u partiji.
        ukupno = int(math.ceil(float(52 - Tablic.inicijalniBrojKarata_stol()) / (self.__n * Tablic.inicijalniBrojKarata_ruka())))

        # Azuriraj broj karata u spilu.
        self.__k -= self.__n * k

        # Ispisi novo dijeljenje.
        print('Dijeljenje {0:d}/{1:d}.'.format(ukupno - int(math.ceil(float(self.__k) / (self.__n * Tablic.inicijalniBrojKarata_ruka()))), ukupno))
        print('Na stolu:')
        print("\t{0:s}\n".format(IOIgrac.lijepiString(sorted(list(stol), reverse = True))))

    def prevediPotez (self, i, igraci, ruka, stol, karta, skupljeno):
        """
        Prevedi potez u tekstualni opis i ispisi ga na stdout.

        Stanje stola i ruke ispisuje se kao u funkciji IOIgrac.odigraj, ali,
        kompaktnosti radi, sam potez se ispisuje kao u funkciji
        IOIgrac.vidiPotez.

        """

        # Prevedi (opisi) potez.

        potez = "{0:s} igra.\n".format(igraci[i].dohvatiIme())

        potez += "Na stolu:\n"
        potez += "\t{0:s}\n".format(IOIgrac.lijepiString(sorted(list(stol), reverse = True)))
        potez += "U ruci:\n"
        potez += "\t{0:s}\n".format(IOIgrac.lijepiString(sorted(list(ruka), reverse = True)))

        potez += "Potez:\n"
        potez += "\t{0:s} {1:s} {2:s}".format(IOIgrac.lijepiString(karta), '<' if skupljeno else '>', IOIgrac.lijepiString(sorted(list(skupljeno), reverse = True)))

        # Ispisi potez.
        print("{0:s}\n".format(potez))

        # Vrati prijevod (opis) poteza.
        return potez

    def kraj (self, rezultat):
        """
        Ispisi rezultat na kraju partije.

        """

        # Dohvati konacni rezultat.
        konacni_rezultat = Tablic.Log.konacniRezultat(rezultat)

        # Ispisi rezultata.
        print('Rezultat:')
        for r, kr in zip(rezultat, konacni_rezultat):
            print("\t{0:s}:".format(r['ime']))
            print("\t\tBodovi: {0:d}".format(r['skupljeno']))
            print("\t\tTable: {0:d}".format(r['table']))
            print("\t\tBroj karata: {0:d}{1:s}".format(r['max'][1], ' [+]' if r['max'][0] else ''))
            print("\t\tUkupno: {0:d}".format(kr))

        # Pronadi igraca sa strogo najvecim brojem bodova ako postoji.
        pobjednik = [0]
        for i in range(1, self.__n):
            if konacni_rezultat[i] > konacni_rezultat[pobjednik[0]]:
                pobjednik = [i]
            elif konacni_rezultat[i] == konacni_rezultat[pobjednik[0]]:
                pobjednik.append(i)

        # Ispisi pobjednika ako postoji igrac sa strogo najvecim brojem bodova odnosno ispisi sve igrace
        # s najvecim brojem bodova inace.
        print('{0:s}:'.format('Pobjednik' if len(pobjednik) == 1 else 'Nerjeseno izmedu'))
        for p in pobjednik:
            print("\t{0:s}".format(rezultat[p]['ime']))

        # Resetiraj relevantne varijable specificne za partiju.
        self.__k = None
        self.__n = None
