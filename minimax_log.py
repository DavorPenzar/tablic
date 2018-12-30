# -*- coding: utf-8 -*-

"""
Implementacija klase zapisnika igre tablic za strojno ucenje minimax algoritma.

"""

import copy

from karta import Karta
from engine import Tablic
from pohlepni_log import PohlepniLog

class MinimaxLog (Tablic.Log):
    """
    Klasa za zapisnik za strojno ucenje minimax algoritma.

    """

    def __init__ (self, log = list()):
        """
        Inicijaliziraj objekt klase MinimaxLog.

        """

        Tablic.Log.__init__(self, log)

    def novaPartija (self, n, igraci):
        pass

    def novoDijeljenje (self, k, stol):
        pass

    def prevediPotez (self, i, igraci, ruka, stol, karta, skupljeno):
        """
        Prevedi potez u format za zapisivanje u zapisnik klase MinimaxLog.

        Povratna vrijednost je objekt klase tuple duljine
        PohlepniLog.dohvatiBrojIndeksa() * len(igraci) +
        3 * PohlepniLog.dohvatiBrojIndeksa() + 4.  U povratnom tuple-u
            1.  na prvom mjestu je zapisano len(igraci), a na drugom mjestu i,
            2.  na sljedecih len(igraci) mjesta zapisani su redom bodovi
                igraca,
            3.  na sljedecih len(igraci) mjesta zapisani su redom borjevi
                skupljenih karata igraca,
            4.  na sljedecem mjestu zapisan je indeks igraca koji je zadnji
                kupio karte sa stola,
            5.  sljedecih PohlepniLog.dohvatiBrojIndeksa() elemenata
                predstavlja karte koje igraci (osim eventualno i-tog) sigurno
                nemaju, a svaki predstavlja broj takvih karata,
            6.  sljedecih (len(igraci) - 1) * PohlepniLog.dohvatiBrojIndeksa()
                elemenata predstavlja karte koje redom svi osim i-tog igraca
                vjerojatno nemaju (svakom igracu pridruzeno je uzastopnih
                PohlepniLog.dohvatiBrojIndeksa() elemenata),
            7.  sljedecih PohlepniLog.dohvatiBrojIndeksa() elemenata
                predstavlja ruku igraca, a oni su 0 ako igrac nema kartu
                odnosno 1 ako ima,
            8.  sljedecih PohlepniLog.dohvatiBrojIndeksa() elemenata
                predstavlja stol, a svaki predstavlja broj odgovarajucih karata
                na stolu,
            9.  sljedeci element predstavlja odigranu kartu,
            10. zadnjih PohlepniLog.dohvatiBrojIndeksa() predstavlja skup
                skupljenih karata, a svaki predstavlja broj takvih karata.
        Skup karata koje igraci sigurno nemaju, ruka, stol, i skupljeno
        reprezentirani su kao skupovi stol u povratnoj vrijednosti
        funkcije PohlepniLog.prevediPotez, a skup karata koje igraci vjerojatno
        nemaju predstavljen je kao skup ruka u povratnoj vrijednosti funkcije
        PohlepniLog.prevediPotez (True u skupu karata koje igrac vjerojatno
        nema znaci da igrac vjerojatno nema tu kartu, a False da mozda ili
        sigurno ima).

        """

        # Pokusaj inicijalizirati varijablu potez na prvih len(igraci) + 3 mjesta, a, ako igraci[i] ne "prepoznaje" trazene
        # metode (ako nije minimax igrac), odustajani i vrati None.
        try:
            potez = [len(igraci), i] + igraci[i].dohvatiBodove() + igraci[i].dohvatiSkupljeno() + [igraci[i].dohvatiZadnjeg()]
        except AttributeError:
            return None

        # Zapis kartu koje igraci sigurno nemaju u potez.
        aux = [0 for j in range(PohlepniLog.dohvatiBrojIndeksa())]
        for x in igraci[i].dohvatiSigurnoNema():
            aux[PohlepniLog.prevediKartu(x)] += 1
        potez += aux

        # Zapisi karte koje igraci vjerojatno nemaju u potez.
        for j in range(len(igraci)):
            if j == i:
                continue
            potez += igraci[i].dohvatiVjerojatnoNema(j)

        # Zapisi ruku u potez.
        aux = [0 for j in range(PohlepniLog.dohvatiBrojIndeksa())]
        for x in ruka:
            aux[PohlepniLog.prevediKartu(x)] += 1
        potez += aux

        # Zapisi stol u potez.
        aux = [0 for j in range(PohlepniLog.dohvatiBrojIndeksa())]
        for x in stol:
            aux[PohlepniLog.prevediKartu(x)] += 1
        potez += aux

        # Zapisi odigranu kartu u potez.
        potez += [PohlepniLog.prevediKartu(karta)]

        # Zapisi skup skupljenih karata u potez.
        aux = [0 for j in range(PohlepniLog.dohvatiBrojIndeksa())]
        for x in skupljeno:
            aux[PohlepniLog.prevediKartu(x)] += 1
        potez += aux

        # Vrati zapisa poteza.
        return tuple(potez)

    def kraj (self, rezultat):
        pass
