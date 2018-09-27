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

    def __copy__ (self):
        return MinimaxLog(self.dohvatiLog(), self.__i)

    def __deepcopy__ (self, memodict = dict()):
        return MinimaxLog(copy.deepcopy(self.dohvatiLog(), memodict))

    def novaPartija (self, n):
        pass

    def novoDijeljenje (self, k):
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
        Skup karata koje igraci sigurno nemaju, stol, ruka i skupljeno
        reprezentirani su kao skupovi ruka, stol u povratnoj vrijednosti
        funkcije PohlepniLog.prevediPotez.  Karte koje igraci vjerojatno nemaju
        slicno su predstavljeni, samo sto su moguce vrijednosti 0 (nije
        vjerojatno da igrac nema takvu kartu) i 1 (igrac vjerojatno nema takvu
        kartu) odnosno None ako su sve takve karte vec u skupu karata koje
        igraci sigurno nemaju.

        """

        # Pokusaj inicijalizacije varijable potez na prvih len(igraci) + 3 mjesta, a, ako igraci[i] ne "prepoznaje" trazene
        # funkcije (ako nije minimax igrac), odustajanje i vracanje None.
        try:
            potez = [len(igraci), i] + igraci[i].dohvatiBodove() + igraci[i].dohvatiSkupljeno() + [igraci[i].dohvatiZadnjeg()]
        except AttributeError:
            return None

        # Zapis karata koje igraci sigurno nemaju u potez.
        aux = [0 for j in range(PohlepniLog.dohvatiBrojIndeksa())]
        for x in igraci[i].dohvatiSigurnoNema():
            aux[PohlepniLog.prevediKartu(x)] += 1
        potez += aux

        # Zapis karata koje igraci vjerojatno nemaju u potez.
        for j in range(len(igraci)):
            if j != i:
                potez += igraci[i].dohvatiVjerojatnoNema(j)

        # Zapis ruke u potez.
        aux = [0 for j in range(PohlepniLog.dohvatiBrojIndeksa())]
        for x in ruka:
            aux[PohlepniLog.prevediKartu(x)] += 1
        potez += aux

        # Zapis stola u potez.
        aux = [0 for j in range(PohlepniLog.dohvatiBrojIndeksa())]
        for x in stol:
            aux[PohlepniLog.prevediKartu(x)] += 1
        potez += aux

        # Zapis odigrane karte u potez.
        potez += [PohlepniLog.prevediKartu(karta)]

        # Zapis skupa skupljenih karata u potez.
        aux = [0 for j in range(PohlepniLog.dohvatiBrojIndeksa())]
        for x in skupljeno:
            aux[PohlepniLog.prevediKartu(x)] += 1
        potez += aux

        # Povrat zapisa poteza.
        return tuple(potez)
