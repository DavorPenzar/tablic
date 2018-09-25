"""
Implementacija klasa zapisnika igre tablic za strojno ucenje pohlepnih alg.

"""

import copy

from karta import Karta
from engine import Tablic

class PohlepniLog1 (Tablic.Log):
    """
    Klasa za zapisnik za ucenje obicnog pohlepnog algoritma.

    """

    @classmethod
    def dohvatiBrojIndeksa (cls) -> int:
        """
        Dohvati broj mogucih indeksa karata za zapisnik.

        Koristeni su svi indeksi od 0 do prethodnika povratne vrijednosti ove funkcije
        i nijedan drugi.

        """

        return 15

    @classmethod
    def prevediKartu (cls, karta : Karta) -> int:
        """
        Prevedi objekt karta u njen indeks za zapsinik.

        Indeks karte je
            0   --  ako je karta A,
            1   --  ako je karta 2 i nije tref 2
            2   --  ako je karta 3,
            3   --  ako je karta 4,
            4   --  ako je karta 5,
            5   --  ako je karta 6,
            6   --  ako je karta 7,
            7   --  ako je karta 8,
            8   --  ako je karta 9,
            9   --  ako je karta 10 i nije karo 10,
            10  --  ako je karta J,
            11  --  ako je karta Q,
            12  --  ako je karta K,
            13  --  ako je karta tref 2,
            14  --  ako je karta karo 10.

        """

        if not isinstance(karta, Karta):
            try:
                karta = Karta(karta)
            except (TypeError, ValueError):
                raise TypeError("karta mora biti objekt klase `Karta'.")

        if karta == Karta(Karta.Boja.TREF, Karta.Znak.BR2):
            return 13
        elif karta == Karta(Karta.Boja.KARO, Karta.Znak.BR10):
            return 14

        return karta.znak.value - (1 if karta.znak.value < 11 else 2)

    @classmethod
    def prevediIndeks (cls, indeks : int):
        if indeks >= 0 and indeks <= 12:
            return Karta.Znak(indeks + (1 if indeks <= 9 else 2))
        elif indeks == 13:
            return Karta(Karta.Boja.TREF, Karta.Znak.BR2)
        elif indeks == 14:
            return Karta(Karta.Boja.KARO, Karta.Znak.BR10)

        return Karta.Znak.NA

    def __init__ (self, log = []):
        """
        Inicijaliziraj objekt klase PohlepniLog1.

        """

        if not isinstance(log, list):
            try:
                log = list(log)
            except (TypeError, ValueError):
                raise TypeError("Objekt log mora biti objekt klase `list'.")

        for potez in log:
            if not isinstance(potez, tuple):
                raise TypeError("Elementi liste log moraju biti objekti tipa `tuple'")
            if len(potez) != 2 * PohlepniLog1.dohvatiBrojIndeksa() + 1:
                raise TypeError('Potezi u listi log moraju biti liste cjelobrojnih vrijednosti duljine 31.')
            for i in range(PohlepniLog1.dohvatiBrojIndeksa()):
                if not isinstance(potez[i], int):
                    raise TypeError("Svaki element liste poteza u listi log mora biti objekt tipa `int'.")
                if not potez[i] in {0, 1}:
                    raise ValueError('Na prvih {0:d} mjesta liste poteza u listi log moraju biti vrijednosti {1:d} i {2:d}.'.format(PohlepniLog1.dohvatiBrojIndeksa(), 0, 1))
            if sum(potez[:PohlepniLog1.dohvatiBrojIndeksa()]) > Tablic.inicijalniBrojKarata_ruka():
                raise ValueError('Suma vrijednosti na prvih {0:d} mjesta liste poteza u listi log ne smije premasiti {1:d}.'.format(PohlepniLog1.dohvatiBrojIndeksa(), Tablic.inicijalniBrojKarata_ruka()))
            for i in range(PohlepniLog1.dohvatiBrojIndeksa(), 2 * PohlepniLog1.dohvatiBrojIndeksa()):
                if not isinstance(potez[i], int):
                    raise TypeError("Svaki element liste poteza u listi log mora biti objekt tipa `int'.")
                if not potez[i] in {0, 1, 2, 3, 4}:
                    raise ValueError('Na drguih {0:d} mjesta liste poteza u listi log moraju biti vrijednosti od {1:d} do {2:d}.'.format(PohlepniLog1.dohvatiBrojIndeksa(), 0, 4))
            if (potez[PohlepniLog1.dohvatiBrojIndeksa() + PohlepniLog1.prevediKartu(Karta(Karta.Znak.BR2))] + potez[PohlepniLog1.dohvatiBrojIndeksa() + PohlepniLog1.prevediKartu(Karta(Karta.Boja.TREF, Karta.Znak.BR2))] > 4 or
                potez[PohlepniLog1.dohvatiBrojIndeksa() + PohlepniLog1.prevediKartu(Karta(Karta.Znak.BR10))] + potez[PohlepniLog1.dohvatiBrojIndeksa() + PohlepniLog1.prevediKartu(Karta(Karta.Boja.KARO, Karta.Znak.BR10))] > 4):
                raise ValueError('Suma vrijednosti na indeksima {0:d} i {1:d} ili {2:d} i {3:d} u listi poteza u listi log ne smije biti strogo veca od {4:d}.'.format(PohlepniLog1.dohvatiBrojIndeksa() + PohlepniLog1.prevediKartu(Karta(Karta.Znak.BR2)), PohlepniLog1.dohvatiBrojIndeksa() + PohlepniLog1.prevediKartu(Karta(Karta.Boja.TREF, Karta.Znak.BR2)),
                                                                                                                                                                       PohlepniLog1.dohvatiBrojIndeksa() + PohlepniLog1.prevediKartu(Karta(Karta.Znak.BR10)), PohlepniLog1.dohvatiBrojIndeksa() + PohlepniLog1.prevediKartu(Karta(Karta.Boja.KARO, Karta.Znak.BR10)),
                                                                                                                                                                       4))
            if not isinstance(potez[2 * PohlepniLog1.dohvatiBrojIndeksa()], int):
                raise TypeError("Svaki element liste poteza u listi log mora biti objekt tipa `int'.")
            if potez[2 * PohlepniLog1.dohvatiBrojIndeksa()] < 0 or potez[2 * PohlepniLog1.dohvatiBrojIndeksa()] > PohlepniLog1.dohvatiBrojIndeksa():
                raise ValueError('Na zadnjem mjestu liste poteza u listi log mora biti vrijednost od {0:d} do {1:d}.'.format(PohlepniLog1.dohvatiBrojIndeksa(), 0, PohlepniLog1.dohvatiBrojIndeksa() - 1))

        Tablic.Log.__init__(self, log)

    def __copy__ (self):
        return PohlepniLog1(self.dohvatiLog())

    def __deepcopy__ (self, memodict = dict()):
        return PohlepniLog1(copy.deepcopy(self.dohvatiLog(), memodict))

    def novaPartija (self, n : int):
        pass

    def novoDijeljenje (self, k : int):
        pass

    def prevediPotez (self, i : int, igraci : list, ruka : set, stol : set, karta : Karta, skupljeno : set) -> list:
        """
        Prevedi potez u format za zapisivanje u zapisnik klase PohlepniLog1.

        Povratna vrijednost je objekt klase list duljine
        2 * PohlepniLog1.dohvatiBrojIndeksa() + 1.  U povratnoj listi
            1.  prvih PohlepniLog1.dohvatiBrojIndeksa() elemenata predstavlja ruku
                igraca, a oni su 0 ako igrac nema kartu odnosno 1 ako ima,
            2.  drugih PohlepniLog1.dohvatiBrojIndeksa() elemenata predstavlja stol, a
                svaki predstavlja broj odgovarajucih karata na stolu,
            3.  zadnji element predstavlja odigranu kartu.
        U prvih PohlepniLog1.dohvatiBrojIndeksa() elemenata karta je reprezentirana
        elementom s indeksom povratnom vrijednosti funkcije PohlepniLog1.prevediKartu,
        a u drugih PohlepniLog1.dohvatiBrojIndeksa() elemenata s indeksom
        PohlepniLog1.dohvatiBrojIndeksa() + povratna vrijednost funkcije
        PohlepniLog1.prevediKartu.  Na zadnjem mjestu karta je reprezentirana povratnom
        vrijednosti funkcije PohelniLog1.prevediKartu.

        """

        potez = [0 for j in range(2 * PohlepniLog1.dohvatiBrojIndeksa() + 1)]

        for x in ruka:
            potez[PohlepniLog1.prevediKartu(x)] = 1

        for x in stol:
            potez[PohlepniLog1.dohvatiBrojIndeksa() + PohlepniLog1.prevediKartu(x)] += 1

        potez[2 * PohlepniLog1.dohvatiBrojIndeksa()] = PohlepniLog1.prevediKartu(karta)

        return tuple(potez)
