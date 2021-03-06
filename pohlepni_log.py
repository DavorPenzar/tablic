# -*- coding: utf-8 -*-

"""
Implementacija klase zapisnika igre tablic za strojno ucenje pohlepnog alg.

"""

import copy

from karta import Karta
from engine import Tablic

class PohlepniLog (Tablic.Log):
    """
    Klasa za zapisnik za strojno ucenje pohlepnog algoritma.

    U biti, zapisnik klase PohlepniLog moze zapisati svaciji potez (neovisno o
    tipu igraca ciji se potez zapisuje) i zapisuje poteze svih igraca u
    partiji, ali format u kojem je potez zapisan napravljen je tako da se iz
    njega moze iscitati zasto bi pohlepni igrac odigrao taj potez ako je to
    uistinu potez pohlepnog igraca.  To jest, za igrace koji ne igraju strogim
    pohlepnim algoritmom (cije odluke o potezima ovise i o nekim drugim
    parametrima, kao slucajnost pri odabiru ili pamcenje koje su karte vec bile
    odigrane), zapis poteza najvjerojatnije ne daje dovoljno informacija o
    potezu odnosno zasto je bas on odabran.

    """

    @classmethod
    def dohvatiBrojIndeksa (cls):
        """
        Dohvati broj mogucih indeksa karata za zapisnik.

        Koristeni su svi indeksi od 0 do prethodnika povratne vrijednosti ove
        funkcije i nijedan drugi.

        """

        return 15

    @classmethod
    def prevediKartu (cls, karta):
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
                raise TypeError("Vrijednost `{0:s}' nije valjana reprezentacija karte.".format(repr(karta)))

        # Tretiraj specijalne slucajeve da je karta neka od karata tref 2 i karo
        # 10.
        if karta.boja == Karta.Boja.TREF and karta.znak == Karta.Znak.BR2:
            return 13
        elif karta.boja == Karta.Boja.KARO and karta.znak == Karta.Znak.BR10:
            return 14

        # Vrati indeks karte.
        return karta.znak.value - (1 if karta.znak < 11 else 2)

    @classmethod
    def prevediIndeks (cls, indeks):
        """
        Prevedi indeks za zapisnik u odgovarajuci znak ili kartu koje definira.

        Metoda je svojevrsni inverz metode PohlepniLog.prevediKartu tako da
            --  sve postojece indekse koji ne ovise o boji karte prevodi u
                objekt klase Karta.Znak,
            --  sve postojece indekse koji ovise o boji karte prevodi u objekt
                klase Karta,
            --  sve nepostojece indekse prevodi u None.

        """

        # Izracunaj i vrati samo znak ako je indeks postojeci i strogo manji od
        # 12, a, ako je postojeci i jednak 13 ili 14, vrati odgovarajucu kartu.
        if indeks >= 0 and indeks <= 12:
            return Karta.Znak(indeks + (1 if indeks < 10 else 2))
        elif indeks == 13:
            return Karta(Karta.Boja.TREF, Karta.Znak.BR2)
        elif indeks == 14:
            return Karta(Karta.Boja.KARO, Karta.Znak.BR10)

        # Vrati None (ako je indeks nepostojeci).
        return None

    def __init__ (self, log = list()):
        """
        Inicijaliziraj objekt klase PohlepniLog.

        """

        Tablic.Log.__init__(self, log)

    def novaPartija (self, n, igraci):
        pass

    def novoDijeljenje (self, k, stol):
        pass

    def prevediPotez (self, i, igraci, ruka, stol, karta, skupljeno):
        """
        Prevedi potez u format za zapisivanje u zapisnik klase PohlepniLog.

        Povratna vrijednost je objekt klase tuple duljine
        2 * PohlepniLog.dohvatiBrojIndeksa() + 1.  U povratnom tuple-u
            1.  prvih PohlepniLog.dohvatiBrojIndeksa() elemenata predstavlja
                ruku igraca, a oni su 0 ako igrac nema kartu odnosno 1 ako ima,
            2.  drugih PohlepniLog.dohvatiBrojIndeksa() elemenata predstavlja
                stol, a svaki predstavlja broj odgovarajucih karata na stolu,
            3.  zadnji element predstavlja odigranu kartu.
        U prvih PohlepniLog.dohvatiBrojIndeksa() elemenata karta je
        reprezentirana elementom s indeksom povratnom vrijednosti funkcije
        PohlepniLog.prevediKartu, a u drugih PohlepniLog.dohvatiBrojIndeksa()
        elemenata s indeksom PohlepniLog.dohvatiBrojIndeksa() + povratna
        vrijednost funkcije PohlepniLog.prevediKartu.  Na zadnjem mjestu karta
        je reprezentirana povratnom vrijednosti funkcije
        PohelniLog1.prevediKartu.

        """

        # Inicijalizaciraj potez na sve vrijednosti 0.
        potez = [0 for j in range(2 * PohlepniLog.dohvatiBrojIndeksa() + 1)]

        # Zapisi ruku u potez.
        for x in ruka:
            potez[PohlepniLog.prevediKartu(x)] = 1

        # Zapisi stol u potez.
        for x in stol:
            potez[PohlepniLog.dohvatiBrojIndeksa() + PohlepniLog.prevediKartu(x)] += 1

        # Zapisi odigranu kartu u potez.
        potez[2 * PohlepniLog.dohvatiBrojIndeksa()] = (PohlepniLog.prevediKartu(karta))

        # Vrati zapis poteza.
        return tuple(potez)

    def kraj (self, rezultat):
        pass
