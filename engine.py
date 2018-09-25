"""
Implementacija klase Tablic za simulaciju igranja igre tablic.

"""

import abc
import copy
import random

import queue

from skupovi import partitivniSkup, unijeDisjunktnih
from karta import Karta

class Tablic (object):
    """
    Klasa za simulaciju igranja igre tablic.

    """

    class Log (object, metaclass = abc.ABCMeta):
        """
        Apstraktna klasa za definiranje portotipa zapisnika partija igre tablic.

        """

        class __Iterator (object):
            """
            Klasa za iteratore za iteriranje po objektu klase Log.

            """

            def __init__ (self, log, unatrag : bool = False):
                """
                Inicijaliziraj iterator za iteriranje po objektu log.

                """

                self.__log = log
                self.__n = len(log)

                if unatrag:
                    self.__i = -1
                    self.__inkr = -1
                else:
                    self.__i = 0
                    self.__inkr = 1

            def __iter__ (self):
                return self

            def __next__ (self):
                if len(self.__log) != self.__n:
                    raise RuntimeError('Duljina zapisnika se promijenila za vrijeme iteriranja.')

                try:
                    x = self.__log[self.__i]
                except KeyError:
                    raise StopIteration()

                self.__i += self.__inkr

                return x

        def __init__ (self, log = [], *args, **kwargs):
            """
            Inicijaliziraj objekt klase Log.

            """

            self.__log = log

        def __copy__ (self):
            """
            Dohvati kopiju zapisnika.

            """

            return Log(self.__log)

        def __deepcopy__ (self, memodict = dict()):
            """
            Dohvati duboku kopiju zapisnika.

            """

            return Log(copy.deepcopy(self.__log, memodict))

        def __len__ (self) -> int:
            """
            Dohvati ukupni broj svih zapisanih poteza.

            """

            return len(self.__log)

        def __iter__ (self) -> __Iterator:
            """
            Iteriraj po zapisniku.

            """

            return Tablic.Log.__Iterator(self)

        def __reversed__ (self) -> __Iterator:
            """
            Iteriraj po zapisniku unatrag.

            """

            return Log.__Iterator(self, unatrag = True)

        def __getitem__ (self, key : int):
            """
            Pokusaj dohvatiti potez.

            """

            if not isinstance(key, int):
                raise TypeError("key mora biti objekt klase `int'.")

            if key >= len(self.__log) or key < -len(self.__log):
                raise KeyError("Ne postoji potez indeksa {0:d}".format(key))

            return copy.deepcopy(self.__log[key])

        def __setitem__ (self, key : int):
            """
            Pokusaj postaviti potez.

            """

            if not isinstance(key, int):
                raise TypeError("key mora biti objekt klase `int'.")

            if key >= len(self.__log) or key < -len(self.__log):
                raise KeyError("Ne postoji potez indeksa {0:d}".format(key))

            raise TypeError('Potezi se ne mogu postavljati manualno.')

        def __delitem__ (self, key : int):
            """
            Pokusaj izbrisati potez.

            """

            if not isinstance(key, int):
                raise TypeError("key mora biti objekt klase `int'.")

            if key >= len(self.__log) or key < -len(self.__log):
                raise KeyError("Ne postoji potez indeksa {0:d}".format(key))

            raise TypeError('Potezi se ne mogu brisati.')

        def __bool__ (self):
            """
            Provjeri je li zapisan neki potez ili ne.

            """

            return bool(self.__log)

        def __repr__ (self) -> str:
            n = len(str(len(self.__log)))

            return '{0:s}(['.format(self.__class__.__name__) + (("\n" + str.join("\n", ["\t{1:{0:d}d}.\t{2:s}".format(n, i, repr(self.__log[i])) for i in range(len(self.__log))]) + "\n") if self.__log else '') + '])'

        def __str__ (self) -> str:
            n = len(str(len(self.__log)))

            return '{0:s}(['.format(self.__class__.__name__) + (("\n" + str.join("\n", ["\t{1:{0:d}d}.\t{2:s}".format(n, i, str(self.__log[i])) for i in range(len(self.__log))]) + "\n") if self.__log else '') + '])'

        def dohvatiLog (self) -> list:
            """
            Dohvati listu svih poteza.

            """

            return copy.deepcopy(self.__log)

        def logirajPotez (self, i : int, igraci : list, ruka : set, stol : set, karta : Karta, skupljeno : set):
            """
            Zapisi potez u zapisnik.

            Ako se potez funkcijom prevediPotez prevodi u None, potez se ne zapisuje.

            """

            potez = self.prevediPotez(i, igraci, ruka, stol, karta, skupljeno)

            if not potez is None:
                self.__log.append(potez)

        @abc.abstractmethod
        def novaPartija (self, n : int):
            """
            Pripremi zapisnik za zapisivanje poteza iz nove partije s n igraca.

            """

            return None

        @abc.abstractmethod
        def novoDijeljenje (self, k : int):
            """
            Pripremi zapisnik za zapisivanje poteza nakon novog dijeljenja k karata.

            """

            return None

        @abc.abstractmethod
        def prevediPotez (self, i : int, igraci : list, ruka : set, stol : set, karta : Karta, skupljeno : set):
            """
            Prevedi potez u format za zapisivanje u zapisnik.

            Objekt igraci lista je kopija igraca redom kojim igraju.

            Ako je povratna vrijednost funkcije None, funkcija logirajPotez ga ne zapisuje.

            """

            return None

    class PrazniLog (Log):
        """
        Klasa za definiranje najjednostavnijeg zapisnika koji ne zapisuje nista.

        """

        def __copy__ (self):
            return PrazniLog(self.dohvatiLog())

        def __deepcopy__ (self, memodict = dict()):
            return PrazniLog(copy.deepcopy(self.dohvatiLog(), memodict))

        def novaPartija (self, n : int):
            pass

        def novoDijeljenje (self, k : int):
            pass

        def prevediPotez (self, i : int, igraci : list, ruka : set, stol : set, karta : Karta, skupljeno : set) -> None:
            """
            Potez se prevodi u None, neovisno o potezu.

            """

            return None

    class Igrac (object, metaclass = abc.ABCMeta):
        """
        Apstraktna klasa za definiranje protoripa igraca igre tablic.

        """

        def __init__ (self, i : int, ime = None, *args, **kwargs):
            """
            Inicijaliziraj objekt klase Igrac.

            Argument i zadaje redni broj igraca u igri (pocevsi od 0).  Argument ime moze
            biti objekt klase str koji zadaje ime igraca, ili None u kojem slucaju se ime
            igraca postavlja na "[klasa igraca] [i]" (na primjer "RandomIgrac 3" za objekt
            klase RandomIgrac i i = 3).

            """

            if not isinstance(i, int):
                raise TypeError("i mora biti objekt klase `int'.")
            if not (ime is None or isinstance(ime, str)):
                raise TypeError("ime mora biti None ili objekt klase `str'.")

            self.__i = i

            if ime is None:
                self.__ime = '{0:s} {1:d}'.format(self.__class__.__name__, i)
            else:
                self.__ime = ime

        def __copy__ (self):
            """
            Dohvati kopiju igraca.

            """

            return Igrac(self.__i, self.__ime)

        def __deepcopy__ (self, memodict = dict()):
            """
            Dohvati duboku kopiju igraca.

            """

            return Igrac(copy.deepcopy(self.__i, memodict), copy.deepcopy(self.__ime, memodict))

        def dohvatiIndeks (self) -> int:
            """
            Dohvati indeks (redni broj u igri) igraca.

            """

            return self.__i

        def dohvatiIme (self) -> str:
            """
            Dohvati ime igraca.

            """

            return self.__ime

        @abc.abstractmethod
        def hocuRazlog (self) -> bool:
            """
            Izjasni zeli li igrac razlog zbog kojega mora ponavljati potez.

            Ako je povratnja vrijednost funkcije True, u slucaju potrebe ponavljanja
            pokusaja igranja poteza argument ponovi ne ce biti objekt klase bool, nego
            tuple koji ce sadrzavati razlog(e) ponavljanja poteza.

            """

            return None

        @abc.abstractmethod
        def saznajBrojIgraca (self, n : int, imena : list):
            """
            Neka igrac sazna da igra u partiji s n igraca (ukljucujuci ovog igraca).

            Objekt imena lista je duljine n i sadrzi redom imena svih n igraca u igri.

            """

            return None

        @abc.abstractmethod
        def saznajNovoDijeljenje (self, ruka : set, stol : set):
            """
            Neka igrac sazna da se izvrsilo novo dijeljenje od k karata svakome.

            """

            return None

        @abc.abstractmethod
        def vidiPotez (self, i : int, stol : set, karta : Karta, skupljeno : set):
            """
            Neka igrac vidi da je igrac s indeksom i odigrao potez.

            """

            return None

        @abc.abstractmethod
        def odigraj (self, ruka : set, stol : set, ponovi = False) -> tuple:
            """
            Neka igrac odigra potez.

            Povratna vrijednost funkcije mora biti tuple oblika
                1.  na indeksu 0 mora biti objekt klase Karta koji se nalazi u skupu ruka i
                    predstavlja kartu koju igrac zeli odigrati,
                2.  na indeksu 1 mora biti objekt klase set koji je podskup skupa stol i
                    predstavlja skup karata koje igrac zeli skupiti sa stola (odnosno je
                    set() ako se ne skuplja nista).

            U slucaju da se trenutni potez pokusava dohbatiti prvi put, argument ponovi bit
            ce False.  U slucaju da je povratna vrijednost ove funkcije predstavljala
            nelegalni potez, funkcija se ponovno poziva tako da je argument ponovi
                1.  True    --  ako je povratna vrijednost funkcije hocuRazlog False,
                2.  tuple   --  ako je povratna vrijednost funkcije hocuRazlog True,
                            --  na indeksu 0 je vrijednost True,
                            --  na indeksu 1 je tuple gresaka zadnjeg pokusaja igranja
                                poteza, a sadrzi
                                --  objekt klase Karta  --  ako se zadnja odigrana karta ne
                                                            nalazi u igracevoj ruci,
                                                        --  povratna karta jednaka je
                                                            odigranoj karti,
                                --  objekt klase set    --  ako skup skupljenih karata nije
                                                            podskup skupa karata na stolu,
                                                        --  povratni skup jednak je
                                                            odigranom skupu,
                                --  objekt klase Karta.Znak --  ako ne postoji podskup
                                                                skupa skupljenih karata
                                                                koji se sumira u znak
                                                                odigrane karte po pravilima
                                                                igre tablic,
                                                            --  povratni znak jednak je
                                                                znaku odigrane karte,
                                --  False   --  ako se skup skupljenih karata ne moze
                                                particionirati na podskupove ciji se svaki
                                                podskup sumira u znak odigrane karte po
                                                pravilima igre Tablic.

            """

            return None

    class RandomIgrac (Igrac):
        """
        Klasa za definiranje najjednostavnijeg igraca koji igra slucajnim odabirom.

        """

        def __copy__ (self):
            return RandomIgrac(self.dohvatiIndeks(), self.dohvatiIme())

        def __deepcopy__ (self, memodict = dict()):
            return RandomIgrac(copy.deepcopy(self.dohvatiIndeks(), memodict), copy.deepcopy(self.dohvatiIme(), memodict))

        def hocuRazlog (self) -> bool:
            return False

        def saznajBrojIgraca (self, n : int, imena : list):
            pass

        def saznajNovoDijeljenje (self, ruka : set, stol : set):
            pass

        def vidiPotez (self, i : int, ruka : set, stol : set, karta : Karta, skupljeno : set):
            pass

        def odigraj (self, ruka : set, stol : int, ponovi = False) -> tuple:
            """
            Neka igrac izvrsi neki (slucajno odabrani) moguci potez.

            """

            # Dohvacanje mogucih poteza.
            M = Tablic.moguciPotezi(stol)

            # Biranje poteza slucajnim odabirom.
            karta = random.choice(list(ruka))
            izbori = (list(unijeDisjunktnih(M[karta.znak])) if karta.znak in M else [frozenset()])
            skupljeno = set(random.choice(izbori))

            # Vracanje odabranog poteza.
            return (karta, skupljeno)

    __noviSpil = {Karta(boja, znak)
                      for boja in {Karta.Boja.HERC,
                                   Karta.Boja.PIK,
                                   Karta.Boja.KARO,
                                   Karta.Boja.TREF}
                      for znak in {Karta.Znak.A,
                                   Karta.Znak.BR2,
                                   Karta.Znak.BR3,
                                   Karta.Znak.BR4,
                                   Karta.Znak.BR5,
                                   Karta.Znak.BR6,
                                   Karta.Znak.BR7,
                                   Karta.Znak.BR8,
                                   Karta.Znak.BR9,
                                   Karta.Znak.BR10,
                                   Karta.Znak.J,
                                   Karta.Znak.Q,
                                   Karta.Znak.K}}

    @classmethod
    def noviSpil (cls) -> set:
        """
        Dohvati novi skup (objekt klase set) svih 52 igrace karte.

        """

        return copy.deepcopy(Tablic.__noviSpil)

    @classmethod
    def inicijalniBrojKarata_stol (cls) -> int:
        """
        Dohvati broj karata na stolu na pocetku igre.

        """

        return 4

    @classmethod
    def inicijalniBrojKarata_ruka (cls) -> int:
        """
        Dohvati najveci broj karata u ruci.

        """

        return 6

    @classmethod
    def vrijednostKarata (cls, x) -> int:
        """
        Izracunaj bodovnu vrijednost karte ili kolekcije karata x.

        Bodovna vrijednost karte definirana je u pravilima igre tablic, i iznosi
            --  1 ako je karta A,
            --  0 ako je karta broj od 2 do 9 i nije tref 2,
            --  1 ako je karta 10 i nije karo 10,
            --  1 ako je karta slika,
            --  1 ako je karta tref 2,
            --  2 ako je karta karo 10.

        Ako je x kolekcija, suma se racuna rekurzivno, stoga je zapravo
            >>> Tablic.vrijednostKarata(((Karta('tref 2'), Karta('karo 10')), Karta('pik A')))
            4

        """

        if isinstance(x, Karta):
            if x == Karta(Karta.Boja.TREF, Karta.Znak.BR2):
                return 1
            if x == Karta(Karta.Boja.KARO, Karta.Znak.BR10):
                return 2
            if x.znak < 10 and x.znak != 1:
                return 0

            return 1

        try:
            return Tablic.vrijednostKarata(Karta(x))
        except (TypeError, ValueError):
            if hasattr(x, '__iter__'):
                vrijednost = 0
                for y in x:
                    vrijednost += Tablic.vrijednostKarata(y)
                return vrijednost
            else:
                raise TypeError("Objekt x mora biti objekt ili kolekcija objekata klase `Karta'.")

    @classmethod
    def vrijednostTable (cls) -> int:
        """
        Dohvati bodovnu vrijednost ostvarenja "table".

        """

        return 1

    @classmethod
    def vrijednostMax (cls) -> int:
        """
        Dohvati bodovnu vrijednost strogo najveceg broja karata na kraju igre.

        """

        return 3

    @classmethod
    def moguciPotezi (cls, S : set) -> dict:
        """
        Pronadi sve moguce sume karata u kolekciji karata S.

        Povratna vrijednost je dict ciji su kljucevi znakovi karata (objekti klase
        Karta.Znak), a vrijednosti objekti klase set elemenata objekata klase frozenset
        elemenata objekata klase Karta.  Svakom kljucu u povratnom rjecniku pridruzena
        je familija podskupova S cija suma u pravilima igre tablic daje (medu ostalim)
        taj znak.

        Ako neki znak nije kljuc povratnog rjecnika, nijedan podskup skupa S ne moze se
        sumirati u taj znak po pravilima igre tablic.

        """

        if not isinstance(S, set):
            try:
                S = set(S)
            except (TypeError, ValueError):
                raise TypeError("S mora biti skup (objekt klase `set').")

        for x in S:
            if not isinstance(x, Karta):
                try:
                    x = Karta(x)
                except (TypeError, ValueError):
                    raise TypeError("Elementi skupa S moraju biti objekti klase `Karta'.")

                break

        M = dict()

        P = partitivniSkup(S)
        P.remove(frozenset())

        for A in P:
            for x in sum(A):
                x = Karta.Znak(x if x != 11 else 1)
                if x in M:
                    M[x] |= {A}
                else:
                    M.update({x : {A}})

        return M

    def __new__ (cls, *args, **kwargs):
        """
        Kreiraj objekt klase Tablic.

        """

        return super(Tablic, cls).__new__(cls)

    def __init__ (self):
        """
        Inicijaliziraj objekt klase Tablic.

        """

        spil = list(copy.deepcopy(Tablic.__noviSpil))
        random.shuffle(spil)

        self.__pokrenuta = False
        self.__zavrsena = False

        self.__spil = queue.Queue()

        for karta in spil:
            self.__spil.put(karta)

        self.__igraci = []
        self.__stol = set()

    def dodajIgraca (self, klasa = RandomIgrac, ime = None, *args, **kwargs):
        """
        Dodaj igraca (objekt klase klasa) u igru.

        Klasa klasa mora biti podklasa klase Tablic.Igrac.

        Argumenti ime, *args, **kwargs prosljeduju se konstruktoru klase klasa pri
        inicijalizaciji novog dodanog igraca.

        """

        if self.__pokrenuta:
            raise TypeError('Nemoguce je dodati igraca u pokrenutu igru.')
        if not issubclass(klasa, Tablic.Igrac):
            raise TypeError('Igrac mora biti objekt podklase klase Igrac.')

        self.__igraci.append({'igrac' : klasa(len(self.__igraci), ime, *args, **kwargs),
                              'ruka' : set(),
                              'skupljeno' : set(),
                              'table' : 0,
                              'max' : False})

    def jePokrenuta (self):
        """
        Provjeri je li igra vec pokrenuta.

        """

        return self.__pokrenuta

    def jeZavrsena (self):
        """
        Provjeri je li igra vec zavrsena.

        """

        return self.__zavrsena

    def dohvatiBrojIgraca (self):
        """
        Dohvati trenutni broj igraca u igri.

        """

        return len(self.__igraci)

    def dohvatiStol (self):
        """
        Dohvati trenutno stanje (sadrzaj) stola u igri.

        """

        return copy.deepcopy(self.__stol)

    def dohvatiIgraca (self, i : int):
        """
        Dohvati igraca s indeksom i.

        Povratna vrijednost je objekt klase i-tog igraca ekvivalentan i-tom igracu u
        igri.

        """

        if not isinstance(i, int):
            try:
                i = int(i)
            except (TypeError, ValueError):
                raise TypeError("i mora biti objekt klase `int'.")

        if i < 0 or i >= len(self.__igraci):
            raise TypeError('Ne postoji igrac s indeksom {0:d}'.format(i))

        return copy.deepcopy(self.__igraci[i]['igrac'])

    def hoceRazlog (self, i : int) -> bool:
        """
        Provjeri zeli li igrac s indeksom i razlog eventualnog ponavljanja poteza.

        """

        if not isinstance(i, int):
            try:
                i = int(i)
            except (TypeError, ValueError):
                raise TypeError("i mora biti objekt klase `int'.")

        if i < 0 or i >= len(self.__igraci):
            raise TypeError('Ne postoji igrac s indeksom {0:d}'.format(i))

        return copy.deepcopy(self.__igraci[i]['igrac'].hocuRazlog())

    def dohvatiIme (self, i : int) -> str:
        """
        Dohvati ime igraca s indeksom i.

        """

        if not isinstance(i, int):
            try:
                i = int(i)
            except (TypeError, ValueError):
                raise TypeError("i mora biti objekt klase `int'.")

        if i < 0 or i >= len(self.__igraci):
            raise TypeError('Ne postoji igrac s indeksom {0:d}'.format(i))

        return copy.deepcopy(self.__igraci[i]['igrac'].dohvatiIme())

    def dohvatiSkupljeno (self, i : int) -> set:
        """
        Dohvati skup dosad skupljenih karata igraca s indeksom i.

        """

        if not isinstance(i, int):
            try:
                i = int(i)
            except (TypeError, ValueError):
                raise TypeError("i mora biti objekt klase `int'.")

        if i < 0 or i >= len(self.__igraci):
            raise TypeError('Ne postoji igrac s indeksom {0:d}'.format(i))

        return copy.deepcopy(self.__igraci[i]['skupljeno'])

    def dohvatiTable (self, i : int) -> int:
        """
        Dohvati broj dosad skupljenih tabli igraca s indeksom i.

        """

        if not isinstance(i, int):
            try:
                i = int(i)
            except (TypeError, ValueError):
                raise TypeError("i mora biti objekt klase `int'.")

        if i < 0 or i >= len(self.__igraci):
            raise TypeError('Ne postoji igrac s indeksom {0:d}'.format(i))

        return copy.deepcopy(self.__igraci[i]['table'])

    def dohvatiMax (self, i : int):
        """
        Saznaj je li igrac s indeksom i skupio strogo najvise karata.

        Ako igra jos nije zavrsila, povratna vrijednost bit ce False.  Ako je igra
        zavrsila, povratna vrijednost bit ce tuple kojemu je na indeksu 0 bool
        vrijednost koja je True ako i samo ako je igrac s indeksom i skupio strogo
        najvise karata, a na indeksu 1 broj skupljenih karata.

        """

        if not isinstance(i, int):
            try:
                i = int(i)
            except (TypeError, ValueError):
                raise TypeError("i mora biti objekt klase `int'.")

        if i < 0 or i >= len(self.__igraci):
            raise TypeError('Ne postoji igrac s indeksom {0:d}'.format(i))

        return copy.deepcopy(self.__igraci[i]['max'])

    def igraj (self, *logovi):
        """
        Odigraj partiju i poteze zapisi u zapisnik log.

        Objekt logovi mora biti tuple objekata podklase klase Tablic.Log.  Ako nije
        zadan nijedan zapisnik, povratna vrijednost funkcije je None.  Ako je zadan
        tocno jedan zapisnik, povratna vrijednost je taj zapisnik.  Inace je povratna
        vrijednpst tuple zapisnika istim redom kojim su dani kao argumenti.

        Nakon pokretanja funkcije funkcija jePokrenuta vracat ce True.

        Nakon izvrsavanja funkcije funkcija jeZavrsena vracat ce True, a dohvatiMax
        vracat ce tuple koji odgovara je li igrac skupio strogo najvise karata i koliko
        je karata skupio.

        Na pocetku izvrsavanja funkcije svim igracima se poziva funkcija
        saznajBrojIgraca s argumentom brojem igraca u trenutnoj partiji.

        """

        def __objaviBrojIgraca ():
            """
            Pozovi Igrac.saznajBrojIgraca na svakom igracu.

            """

            imena = [self.__igraci[i]['igrac'].dohvatiIme() for i in range(len(self.__igraci))]

            for i in range(len(self.__igraci)):
                self.__igraci[i]['igrac'].saznajBrojIgraca(len(self.__igraci), copy.deepcopy(imena))

        def __pokreni ():
            """
            Postavi __pokrenuta na True i smjesti 4 inicijalne karte na stol.
            """

            self.__pokrenuta = True

            for i in range(Tablic.inicijalniBrojKarata_stol()):
                self.__stol |= {self.__spil.get()}

        def __zavrsi (zadnji):
            """
            Postavi __zavrsena na True, pocisti stol i pronadi max skupljenih karata.

            """

            self.__zavrsena = True

            # Pocisti stol
            if not zadnji is None:
                while self.__stol:
                    karta = self.__stol.pop()
                    self.__igraci[zadnji]['skupljeno'] |= {karta}

            # Pronadi igraca sa strogo najvise karata.

            I = [0]
            self.__igraci[0]['max'] = (False, len(self.__igraci[0]['skupljeno']))
            for j in range(1, len(self.__igraci)):
                self.__igraci[j]['max'] = (False, len(self.__igraci[j]['skupljeno']))
                if (len(self.__igraci[j]['skupljeno']) == len(self.__igraci[I[0]]['skupljeno'])):
                    I.append(j)
                elif (len(self.__igraci[j]['skupljeno']) > len(self.__igraci[I[0]]['skupljeno'])):
                    I = [j]

            if len(I) == 1:
                self.__igraci[I[0]]['max'] = (True, len(self.__igraci[I[0]]['skupljeno']))

        def __podijeli ():
            """
            Podijeli svim igracima jednak broj karata (sto vise, a najvise 6).

            """

            for i in range(Tablic.inicijalniBrojKarata_ruka()):
                for j in range(len(self.__igraci)):
                    if self.__spil.empty():
                        break
                    self.__igraci[j]['ruka'] |= {self.__spil.get()}
                if self.__spil.empty():
                    return i + 1

            return 6

        def __objaviNovoDijeljenje (stol : set):
            """
            Pozovi Igrac.saznajNovoDijeljenje na svakom igracu.

            """

            for i in range(len(self.__igraci)):
                self.__igraci[i]['igrac'].saznajNovoDijeljenje(copy.deepcopy(self.__igraci[i]['ruka']), copy.deepcopy(stol))

        def __legalniPotez (i : int, karta : Karta, skupljeno : set, razlog : bool = False):
            """
            Provjeri je li potez igraca s indeksom i legalan.

            Ako je razlog False, povratna vrijednost je bool vrijednosti True ako i samo
            ako je potez legalan.  Ako je razlog True, u slucaju ilegalnog poteza povratna
            vrijednost je tuple kojemu je na indeksu 0 False, a na tuple s razlozima
                --  ako igrac s indeksom i u ruci nema kartu karta, tuple razloga ce
                    sadrzavati objekt karta,
                --  ako skup skupljeno nije podskup trenutnog skupa karata na stolu, tuple
                    razloga ce sadrzavati objekt skupljeno,
                --  ako ne postoji podskup skupa skupljeno koji se moze sumirati u znak
                    karte karta, tuple razloga ce sadrzavati karta.znak,
                --  ako se skup karata skupljeno ne moze podijeliti na particiju ciji se
                    svaki clan moze sumirati u znak karte karta, tuple razloga ce
                    sadrzavati False.
            Sume karata racunaju se po pravilima igre tablic.

            """

            greske = []

            # Provjeri je li karta u ruci.
            if not karta in self.__igraci[i]['ruka']:
                greske.append(karta)

            # Provjeri je li skupljeno na stolu.
            if not skupljeno.issubset(self.__stol):
                greske.append(skupljeno)

            # Ako se skuplja sa stola, provjeri sume.
            if skupljeno:
                M = Tablic.moguciPotezi(skupljeno)

                if not karta.znak in M:
                    greske.append(karta.znak)
                else:
                    U = unijeDisjunktnih(M[karta.znak])

                    if not frozenset(skupljeno) in U:
                        greske.append(False)

            # Ako treba, vrati ilegalnost poteza i greske.
            if razlog and greske:
                return (False, tuple(greske))

            # Vrati legalnost poteza.
            return not bool(greske)

        def __dohvatiPotez (i : int) -> tuple:
            """
            Zovi Igrac.odigraj s na igracu i do prvog legalnog poteza.

            """

            ponovi = False
            razlog = None

            while True:
                karta, skupljeno = self.__igraci[i]['igrac'].odigraj(copy.deepcopy(self.__igraci[i]['ruka']), copy.deepcopy(self.__stol), ponovi)
                legalno = __legalniPotez(i, karta, skupljeno, self.__igraci[i]['igrac'].hocuRazlog())
                if isinstance(legalno, tuple):
                    legalno, razlog = legalno

                if legalno:
                    break
                elif razlog is None:
                    ponovi = True
                else:
                    ponovi = (True, razlog)

            return (karta, skupljeno)

        def __objaviPotez (i : int, karta : Karta, skupljeno : set):
            """
            Pozovi Igrac.vidiPotez na svakom igracu.

            """

            for j in range(len(self.__igraci)):
                self.__igraci[j]['igrac'].vidiPotez(i, copy.deepcopy(self.__igraci[j]['ruka']), copy.deepcopy(self.__stol), karta, copy.deepcopy(skupljeno))

        def __uzmiIzRuke (i : int, karta : Karta, skupi : bool):
            """
            Makni kartu iz ruke igraca.

            Ako je skupi = True, karta se stavlja u igracev skup skupljenih karata.  Inace
            se karta stavlja na stol.

            """

            self.__igraci[i]['ruka'].remove(karta)
            if skupi:
                self.__igraci[i]['skupljeno'] |= {karta}
            else:
                self.__stol |= {karta}

        def __uzmiSaStola (i : int, skupljeno : set):
            """
            Makni kartu sa stola i stavi ju u skup skupljenih karata igraca.

            """

            for karta in skupljeno:
                self.__stol.remove(karta)
                self.__igraci[i]['skupljeno'] |= {karta}

        def __provjeriTablu (i : int):
            """
            Ako je nakon igracevog poteza stol prazan, dodaj mu tablu.

            """

            if not self.__stol:
                self.__igraci[i]['table'] += 1

        # Provjeri argument funkcije i stanje igre.

        logovi = list(logovi)

        for i in range(len(logovi)):
            if not issubclass(type(logovi[i]), Tablic.Log):
                raise TypeError("Zapisnici moraju biti objekti podklase klase `Tablic.Log'.")

        if self.__pokrenuta:
            raise TypeError('Trenutna partija vec je pokrenuta.')

        if not self.__igraci:
            raise TypeError('Trenutna partija nema igraca.')

        if len(self.__igraci) == 1 or (52 - Tablic.inicijalniBrojKarata_stol()) % len(self.__igraci):
            raise TypeError('{0:d} nije valjani broj igraca u partiji igre tablic.'.format(len(self.__igraci)))

        # Pokreni partiju.
        __pokreni()

        # Logiraj i objavi pocetak nove partije.
        for i in range(len(logovi)):
            logovi[i].novaPartija(len(self.__igraci))
        __objaviBrojIgraca()

        # Igraj partiju.

        zadnji = None
        while not self.__spil.empty():
            # Podijeli, logiraj i objavi novo dijeljenje.
            k = __podijeli()
            for i in range(len(logovi)):
                logovi[i].novoDijeljenje(k)
            __objaviNovoDijeljenje(self.__stol)

            while self.__igraci[0]['ruka']:
                for i in range(len(self.__igraci)):
                    # Dohvati, logiraj i objavi potez.
                    karta, skupljeno = __dohvatiPotez(i)
                    for j in range(len(logovi)):
                        logovi[j].logirajPotez(copy.deepcopy(i), [copy.deepcopy(self.__igraci[k]['igrac']) for k in range(len(self.__igraci))], copy.deepcopy(self.__igraci[i]['ruka']), copy.deepcopy(self.__stol), copy.deepcopy(karta), copy.deepcopy(skupljeno))
                    __objaviPotez(i, karta, skupljeno)

                    # Promijeni stanje igre ovisno o potezu.
                    __uzmiIzRuke(i, karta, bool(skupljeno))
                    if skupljeno:
                        __uzmiSaStola(i, skupljeno)
                        __provjeriTablu(i)
                        zadnji = i

        # Zavrsi partiju.
        __zavrsi(zadnji)

        # Vracanje odgovarajuce povratne vrijednosti.

        if not logovi:
            return None

        if len(logovi) == 1:
            return logovi[0]

        return tuple(logovi)

    def dohvatiRezultat (self) -> list:
        """
        Dohvati trenutne rezultate igraca.

        Povratna vrijednost je objekt klase list kojemu je na indeksu i >= 0 zapisan
        rezultat igraca s indeksom i.  Svaki element povratne liste je objekt klase
        dict s kljucevima i vrijednostima
            --  'ime' : ime igraca,
            --  'skupljeno' : bodovna vrijednost skupa skupljenih karata,
            --  'table' : broj skupljenih tabli,
            --  'max' : je li skupio strogo najvise karata.

        """

        rezultati = []

        for i in range(len(self.__igraci)):
            r = {'ime' : self.__igraci[i]['igrac'].dohvatiIme(),
                 'skupljeno' : 0,
                 'table' : self.__igraci[i]['table'],
                 'max' : self.__igraci[i]['max']}
            for karta in self.__igraci[i]['skupljeno']:
                r['skupljeno'] += Tablic.vrijednostKarata(karta)
            rezultati.append(r)

        return rezultati
