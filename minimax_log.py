import copy

from karta import Karta
from engine import Tablic
from pohlepni_log import PohlepniLog1
from minimax_igrac import MinimaxIgrac1

class MinimaxLog1 (Tablic.Log):
    def __init__ (self, log = []):
        Tablic.Log.__init__(self, log)

        self.__n = None

    def __copy__ (self):
        return MinimaxLog1(self.dohvatiLog(), self.__i)

    def __deepcopy__ (self, memodict = dict()):
        return MinimaxLog1(copy.deepcopy(self.dohvatiLog(), memodict), copy.deepcopy(self.__i, memodict))

    def novaPartija (self, n : int):
        self.__n = n

    def novoDijeljenje (self, k : int):
        pass

    def prevediPotez (self, i : int, igraci : list, ruka : set, stol : set, karta : Karta, skupljeno : set) -> list:
        if not isinstance(igraci[i], MinimaxIgrac1):
            return None

        potez = []

        potez += igraci[i].dohvatiBodove()
        potez += igraci[i].dohvatiSkupljeno()
        potez += [igraci[i].dohvatiZadnjeg() if not igraci[i].dohvatiZadnjeg() is None else -1]

        aux = [0 for j in range(PohlepniLog1.dohvatiBrojIndeksa())]
        for x in igraci[i].dohvatiSigurnoNema():
            aux[PohlepniLog1.prevediKartu(x)] += 1
        potez += aux

        for j in range(len(igraci)):
            if j != i:
                potez += igraci[i].dohvatiVjerojatnoNema(j)

        aux = [0 for j in range(PohlepniLog1.dohvatiBrojIndeksa())]
        for x in ruka:
            aux[PohlepniLog1.prevediKartu(x)] += 1
        potez += aux

        aux = [0 for j in range(PohlepniLog1.dohvatiBrojIndeksa())]
        for x in stol:
            aux[PohlepniLog1.prevediKartu(x)] += 1
        potez += aux

        potez += [PohlepniLog1.prevediKartu(karta)]

        aux = [0 for j in range(PohlepniLog1.dohvatiBrojIndeksa())]
        for x in skupljeno:
            aux[PohlepniLog1.prevediKartu(x)] += 1
        potez += aux

        return tuple(potez)
