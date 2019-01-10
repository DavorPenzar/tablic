# -*- coding: utf-8 -*-

"""
Implementacija klase Tablic za simulaciju igranja igre tablic.

"""

import abc
import copy
import random
import six

import queue

from skupovi import partitivniSkup, unijeDisjunktnih
from karta import Karta

if six.PY3:
    unicode = str

class Tablic (object):
    """
    Klasa za simulaciju igranja igre tablic.

    """

    @six.add_metaclass(abc.ABCMeta)
    class Log (object):
        """
        Apstraktna klasa za definiranje portotipa zapisnika igre tablic.

        """

        class __Iterator (object):
            """
            Klasa za iteratore za iteriranje po objektu klase Log.

            """

            def __init__ (self, log, start = 0, stop = None, step = 1):
                """
                Inicijaliziraj iterator za iteriranje po objektu log.

                """

                self.__log = log

                self.__i = start
                self.__stop = len(self.__log) if stop is None else stop
                self.__step = step

            def __copy__ (self):
                """
                Dohvati copy.copy(self).

                """

                return __Iterator(self.__log, self.__i, self.__stop, self.__step)

            def __deepcopy__ (self, memodict = dict()):
                """
                Dohvati copy.deepcopy(self, memodict).

                """

                return __Iterator(copy.deepcopy(self.__log, memodict),
                                  copy.deepcopy(self.__i, memodict),
                                  copy.deepcopy(self.__stop, memodict),
                                  copy.deepcopy(self.__step, memodict))

            def __iter__ (self):
                """
                Dohvati iter(self).

                """

                return self

            def next (self):
                """
                Dohvati next(self).

                """

                if self.__step >= 0 and self.__i >= self.__stop or self.__step <= 0 and self.__i <= self.__stop:
                    raise StopIteration()

                try:
                    x = self.__log[self.__i]
                except KeyError:
                    raise StopIteration()

                self.__i += self.__step

                return x

            __next__ = next

            def __repr__ (self):
                """
                Dohvati repr(self).

                """

                return '<{0:s}: ({1:s}, {2:d}, {3:d}, {4:d})>'.format(self.__class__.__name__, repr(self.__log), self.__i, self.__stop, self.__step)

            def __str__ (self):
                """
                Dohvati str(self).

                """

                return '{0:s}({1:s}, {2:d}, {3:d}, {4:d})'.format(self.__class__.__name__, str(self.__log), self.__i, self.__stop, self.__step)

            def __unicode__ (self):
                """
                Dohvati unicode(self).

                """

                return unicode('{0:s}({1:s}, {2:d}, {3:d}, {4:d})').format(self.__class__.__name__, unicode(self.__log), self.__i, self.__stop, self.__step)

        @classmethod
        def konacniRezultat (cls, rezultat):
            """
            Izracunaj konacni rezultat partije igre tablic.

            Objekt rezultat sukladan je povratnoj vrijednosti funkcije
            Tablic.dohvatiRezultat.

            Povratna vrijednost funkcije Tablic.dohvatiRezultat rezultate
            predstavlja "razlomljeno", to jest posebno prikazuje broj
            skupljenih bodova skupljenim kartama, broj ostvarenih tabli i
            otkriva koji je igrac skupio strogo najvise karata.  Povratna
            vrijednost ove funkcije lista je jedinstvenih nenegativnih
            cjelobrojnih vrijednosti koje zbrajaju bodove koje su igraci
            skupili na pojedinom elementu igre.

            """

            return [r['skupljeno'] + r['table'] * Tablic.vrijednostTable() + int(r['max'][0]) * Tablic.vrijednostMax() for r in rezultat]

        def __init__ (self, log = list()):
            """
            Inicijaliziraj objekt klase Log.

            Svaka klasa derivirana od klase Tablic.Log, ako inicijalizira
            vlastitu metodu __init__, ta bi metoda trebala biti oblika
                >>> def __init__ (self, log = list()[, ...]):
                        Tablic.Log.__init__(self, log)
                        [...]
            pri cemu za argument log ne bi smio biti prosljedeni objekt koji
            nisu tipa list, a eventualni ostali argumenti bi trebali imati
            zadane vrijednosti.

            """

            self.__log = log

        def __copy__ (self):
            """
            Dohvati copy.copy(self).

            """

            return self.__class__(self.__log)

        def __deepcopy__ (self, memodict = dict()):
            """
            Dohvati copy.deepcopy(self).

            """

            return self.__class__(copy.deepcopy(self.__log, memodict))

        def __len__ (self):
            """
            Dohvati ukupni broj svih zapisanih poteza.

            """

            return len(self.__log)

        def __iter__ (self):
            """
            Iteriraj po zapisniku.

            """

            return Tablic.Log.__Iterator(self, *slice(None, None, 1).indices(len(self)))

        def __reversed__ (self):
            """
            Iteriraj po zapisniku unatrag.

            """

            return Log.__Iterator(self, *slice(None, None, -1).indices(len(self)))

        def __getitem__ (self, key):
            """
            Pokusaj dohvatiti potez.

            """

            if isinstance(key, slice):
                return list(Log.__Iterator(self, *key.indices(len(self))))

            return copy.deepcopy(self.__log[key])

        def __setitem__ (self, key):
            """
            Pokusaj postaviti potez.

            """

            raise TypeError('Potezi se ne mogu postavljati manualno.')

        def __delitem__ (self, key):
            """
            Pokusaj izbrisati potez.

            """

            raise TypeError('Potezi se ne mogu brisati.')

        def __nonzero__ (self):
            """
            Provjeri je li zapisan neki potez ili ne.

            """

            return bool(self.__log)

        __bool__ = __nonzero__

        def __repr__ (self):
            """
            Dohvati repr(self).

            """

            # Izracunaj najveci broj znamenki potreban za ispis rednog broja
            # poteza u zapisniku.
            n = len(str(len(self.__log) - 1))

            return '<{0:s}: [{1:s}]>'.format(self.__class__.__name__, "\n{0:s}\n".format(str.join("\n", ["\t{1:{0:d}d}.\t{2:s}".format(n, i, repr(self.__log[i])) for i in range(len(self.__log))])) if self.__log else '')

        def __str__ (self):
            """
            Dohvati str(self).

            """

            # Izracunaj najveci broj znamenki potreban za ispis rednog broja
            # poteza u zapisniku.
            n = len(str(len(self.__log) - 1))

            return '{0:s}([{1:s}])'.format(self.__class__.__name__, "\n{0:s}\n".format(str.join("\n", ["\t{1:{0:d}d}.\t{2:s}".format(n, i, str(self.__log[i])) for i in range(len(self.__log))])) if self.__log else '')

        def __unicode__ (self):
            """
            Dohvati unicode(self).

            """

            # Izracunaj najveci broj znamenki potreban za ispis rednog broja
            # poteza u zapisniku.
            n = len(str(len(self.__log) - 1))

            return unicode('{0:s}([{1:s}])').format(self.__class__.__name__, "\n{0:s}\n".format(unicode.join(unicode("\n"), ["\t{1:{0:d}d}.\t{2:s}".format(n, i, unicode(self.__log[i])) for i in range(len(self.__log))])) if self.__log else '')

        def dohvatiLog (self):
            """
            Dohvati listu svih poteza.

            """

            return copy.deepcopy(self.__log)

        def spremi (self, izlaz, razmak = "\n", tip = 'str'):
            """
            Ispisi sve poteze u datotek.

            Ako je izlaz objekt klase string ili unicode, za izlaznu datoteku
            otvara se datoteka imena jednakog vrijednosti varijable izlaz i to
            s nacinom 'w' (sav eventualni prijasnji sadrzaj datoteke se brise).
            Inace se varijabla izlaz smatra izlaznom datotekom (u koju se
            ispisuje).  Ispis se vrsi pozivom
                >>> izlaz.write(...)
            gdje je kao argument dan string za ispis. Pri (uspjesnom) zavrsetku
            funkcije izlazna se datoteka nuzno zatvara pozivom
                >>> izlaz.close()

            Potezi su odvojeni stringom razmak (ako je razmak = '', potezi nisu
            odvojeni uopce, ni razmakom ni prelaskom u novi red; ako potezi
            moraju biti odvojeni praznim redom, onda varijabla razmak mora
            imati vrijednost "\n\n").  Potezi se u ispis konvertiraju ovisno o
            vrijednosti varijable tip, i to po sljedecem pravilu:
                --  tip = 'repr'    --  ispisuje se repr(potez),
                --  tip = 'str' --  ispisuje se str(potez),
                --  tip = 'unicode' --  ispisuje se unicode(potez),
                --  inace se ispisuje ''.

            """

            # Otvaranje izlazne datoteke po potrebi.
            if isinstance(izlaz, (str, unicode)):
                izlaz = open(izlaz, 'w')

            # Detekcija nacina ispisa poteza.
            konverzija = lambda x : ''
            if tip == 'repr':
                konverzija = lambda x : repr(x)
            elif tip == 'str':
                konverzija = lambda x : str(x)
            elif tip == 'unicode':
                konverzija = lambda x : unicode(x)

            # Ispis svih poteza.
            for potez in self.__log:
                izlaz.write(konverzija(potez))
                izlaz.write(razmak)

            # Zatvaranje izlazne datoteke.
            izlaz.close()

        def logirajPotez (self, i, igraci, ruka, stol, karta, skupljeno):
            """
            Zapisi potez u zapisnik.

            Ako se potez funkcijom prevediPotez prevodi u None, potez se ne
            zapisuje.

            """

            # Prevedi potez.
            potez = self.prevediPotez(i, igraci, ruka, stol, karta, skupljeno)

            if potez is None:
                # Ako je prijevod rezultirao vrijednosti None, ne zapisi ga.
                return

            # Zapisi potez u zapisnik.
            self.__log.append(potez)

        @abc.abstractmethod
        def novaPartija (self, n, igraci):
            """
            Pripremi zapisnik za zapisivanje poteza iz nove partije.

            Lista igraci (duljine n) kopija je igraca koji sudjeluju u partiji
            redoslijedom kojim su na potezu.

            """

            return None

        @abc.abstractmethod
        def novoDijeljenje (self, k, stol):
            """
            Pripremi zapisnik za zapisivanje poteza nakon novog dijeljenja.

            Broj k oznacava broj podijeljenih karata svakom igracu, a skup stol
            oznacava trenutno stanje stola.

            """

            return None

        @abc.abstractmethod
        def prevediPotez (self, i, igraci, ruka, stol, karta, skupljeno):
            """
            Prevedi potez u format za zapisivanje u zapisnik.

            Objekt igraci lista je kopija igraca redom kojim igraju.

            Ako je povratna vrijednost funkcije None, funkcija logirajPotez ga
            ne zapisuje.

            """

            return None

        @abc.abstractmethod
        def kraj (self, rezultat):
            """
            Saznaj za kraj i rezultat partije.

            Objekt rezultat sukladan je povratnoj vrijednosti funkcije
            Tablic.dohvatiRezultat, a objekt klase Tablic ga nad zapisnikom
            poziva na kraju partije (kada je igracu koji je skupio strogo
            najvise karata (ako takav postoji) to i zapisano).

            """

            return None

    class PrazniLog (Log):
        """
        Klasa za definiranje najjednostavnijeg zapisnika (ne zapisuje nista).

        """

        def novaPartija (self, n, igraci):
            pass

        def novoDijeljenje (self, k, stol):
            pass

        def prevediPotez (self, i, igraci, ruka, stol, karta, skupljeno):
            """
            Potez se prevodi u None, neovisno o potezu.

            """

            return None

        def kraj (self, rezultat):
            pass

    @six.add_metaclass(abc.ABCMeta)
    class Igrac (object):
        """
        Apstraktna klasa za definiranje protoripa igraca igre tablic.

        """

        def __init__ (self, i, ime = None):
            """
            Inicijaliziraj objekt klase Igrac.

            Argument i zadaje redni broj igraca u partiji (pocevsi od 0).
            Argument ime moze biti objekt klase str koji zadaje ime igraca, ili
            None u kojem slucaju se ime igraca postavlja na
            "[klasa igraca] [i + 1]" (na primjer "RandomIgrac 3" za objekt
            klase RandomIgrac i i = 2).

            Svaka klasa derivirana od klase Tablic.Igrac, ako inicijalizira
            vlastitu metodu __init__, ta bi metoda trebala biti oblika
                >>> def __init__ (self, i, ime = None[, ...]):
                        Tablic.Igrac.__init__(self, i, ime)
                        [...]
            pri cemu za argument i ne bi smio biti prosljeden objekt koji nije
            tipa int (metoda Tablic.dodajIgraca ionako prosljeduje samo takav
            argument na prvo mjesto), za argument ime ne bi smio biti
            prosljeden objekti koji nije None ili tipa str, a ostali argumenti
            bi trebali imati zadane vrijednosti.

            """

            self.__i = i

            if ime is None:
                self.__ime = '{0:s} {1:d}'.format(self.__class__.__name__, i + 1)
            else:
                self.__ime = ime

        def __copy__ (self):
            """
            Dohvati copy.copy(self).

            """

            return self.__class__(self.__i, self.__ime)

        def __deepcopy__ (self, memodict = dict()):
            """
            Dohvati copy.deepcopy(self, memodict).

            """

            return self.__class__(copy.deepcopy(self.__i, memodict), copy.deepcopy(self.__ime, memodict))

        def __repr__ (self):
            """
            Dohvati repr(self).

            """

            return '<{0:s}: ({1:d}, {2:s})>'.format(self.__class__.__name__, self.__i, repr(self.__ime))

        def __str__ (self):
            """
            Dohvati str(self).

            """

            return '{0:s}({1:s})'.format(self.__class__.__name__, repr(self.__ime))

        def __unicode__ (self):
            """
            Dohvati unicode(self).

            """

            return unicode(str(self))

        def dohvatiIndeks (self):
            """
            Dohvati indeks (redni broj u partiji) igraca.

            """

            return self.__i

        def dohvatiIme (self):
            """
            Dohvati ime igraca.

            """

            return self.__ime

        @abc.abstractmethod
        def hocuRazlog (self):
            """
            Izjasni zeli li igrac razlog zbog kojega mora ponavljati potez.

            Ako je povratnja vrijednost funkcije True, u slucaju potrebe
            ponavljanja pokusaja igranja poteza argument ponovi ne ce biti
            objekt klase bool, nego tuple koji ce sadrzavati razlog(e)
            ponavljanja poteza.

            """

            return None

        @abc.abstractmethod
        def saznajBrojIgraca (self, n, imena):
            """
            Neka igrac sazna da igra u partiji s n igraca.

            Objekt imena lista je duljine n i sadrzi redom imena svih n igraca
            u partiji (igrac je jedan od tih n igraca).

            """

            return None

        @abc.abstractmethod
        def saznajNovoDijeljenje (self, ruka, stol):
            """
            Neka igrac sazna da se izvrsilo novo dijeljenje.

            Skup stol prikazuje trenutno stanje stola, a skup ruka trenutno
            stanje igraceve ruke.

            """

            return None

        @abc.abstractmethod
        def vidiPotez (self, i, ruka, stol, karta, skupljeno):
            """
            Neka igrac vidi da je igrac s indeksom i odigrao potez.

            Skup ruka skup je karata koje (ovaj) igrac ima u ruci, a ne koje
            karte u ruci ima igrac koji je odigrao potez.

            """

            return None

        @abc.abstractmethod
        def saznajRezultat (self, rezultat):
            """
            Neka igrac vidi konacni rezultat na kraju partije.

            Objekt rezultat sukladan je povratnoj vrijednosti funkcije
            Tablic.dohvatiRezultat, a objekt klase Tablic ga nad zapisnikom
            poziva na kraju partije (kada je igracu koji je skupio strogo
            najvise karata (ako takav postoji) to i zapisano).

            """

            return None

        @abc.abstractmethod
        def odigraj (self, ruka, stol, ponovi = False):
            """
            Neka igrac odigra potez.

            Povratna vrijednost funkcije mora biti tuple oblika
                1.  na indeksu 0 mora biti objekt klase Karta koji se nalazi u
                    skupu ruka i predstavlja kartu koju igrac zeli odigrati,
                2.  na indeksu 1 mora biti objekt klase set koji je podskup
                    skupa stol i predstavlja skup karata koje igrac zeli
                    skupiti sa stola (odnosno je set() ako se ne skuplja
                    nista).

            U slucaju da se trenutni potez pokusava dohbatiti prvi put,
            argument ponovi bit ce False.  U slucaju da je povratna vrijednost
            ove funkcije predstavljala nelegalni potez, funkcija se ponovno
            poziva tako da je argument ponovi
                1.  True    --  ako je povratna vrijednost funkcije hocuRazlog
                                False,
                2.  tuple   --  ako je povratna vrijednost funkcije hocuRazlog
                                True,
                            --  na indeksu 0 je vrijednost True,
                            --  na indeksu 1 je tuple gresaka zadnjeg pokusaja
                                igranja poteza, a sadrzi
                                --  objekt klase Karta  --  ako se zadnja
                                                            odigrana karta ne
                                                            nalazi u igracevoj
                                                            ruci,
                                                        --  povratna karta
                                                            jednaka je
                                                            odigranoj karti,
                                --  objekt klase set    --  ako skup skupljenih
                                                            karata nije podskup
                                                            skupa karata na
                                                            stolu,
                                                        --  povratni skup
                                                            jednak je odigranom
                                                            skupu,
                                --  objekt klase Karta.Znak --  ako ne postoji
                                                                podskup skupa
                                                                skupljenih
                                                                karata koji se
                                                                sumira u znak
                                                                odigrane karte
                                                                po pravilima
                                                                igre tablic,
                                                            --  povratni znak
                                                                jednak je znaku
                                                                odigrane karte,
                                --  False   --  ako se skup skupljenih karata
                                                ne moze particionirati na
                                                podskupove ciji se svaki
                                                podskup sumira u znak odigrane
                                                karte po pravilima igre tablic.

            """

            return None

    class RandomIgrac (Igrac):
        """
        Klasa za definiranje najjednostavnijeg igraca (igra sl. odabirom).

        """

        def hocuRazlog (self):
            return False

        def saznajBrojIgraca (self, n, imena):
            pass

        def saznajNovoDijeljenje (self, ruka, stol):
            pass

        def vidiPotez (self, i, ruka, stol, karta, skupljeno):
            pass

        def saznajRezultat (self, rezultat):
            pass

        def odigraj (self, ruka, stol, ponovi = False):
            """
            Neka igrac izvrsi neki (slucajno odabrani) moguci potez.

            """

            # Dohvati moguce poteze.
            M = Tablic.moguciPotezi(stol)

            # Odaberi potez slucajnim odabirom.
            karta = random.choice(list(ruka))
            izbori = list(unijeDisjunktnih(M[karta.znak])) if karta.znak in M else [frozenset()]
            skupljeno = set(random.choice(izbori))

            # Vrati odabrani potez.
            return (karta, skupljeno)

    @classmethod
    def inicijalniBrojKarata_stol (cls):
        """
        Dohvati broj karata na stolu na pocetku partije.

        """

        return 4

    @classmethod
    def inicijalniBrojKarata_ruka (cls):
        """
        Dohvati najveci broj karata u ruci.

        """

        return 6

    @classmethod
    def vrijednostKarata (cls, x):
        """
        Izracunaj bodovnu vrijednost karte ili kolekcije karata x.

        Bodovna vrijednost karte definirana je u pravilima igre tablic, i
        iznosi
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

        # Vrati bodovnu vrijednost karte x ako je x karta.
        if isinstance(x, Karta):
            if x.boja is Karta.Boja.TREF and x.znak is Karta.Znak.BR2:
                return 1
            if x.boja is Karta.Boja.KARO and x.znak is Karta.Znak.BR10:
                return 2
            if x.znak < 10 and x.znak != 1:
                return 0

            return 1

        # Konvertiraj x u kartu i vracati njezinu bodovnu vrijednost odnosno vrati sumu bodovnih
        # vrijednosti karata u kolekciji x ako x nije nonvertibilno u kartu.
        try:
            return Tablic.vrijednostKarata(Karta(x))
        except (TypeError, ValueError):
            if hasattr(x, '__iter__'):
                return sum(Tablic.vrijednostKarata(y) for y in x)
            else:
                raise TypeError("Objekt x mora biti objekt ili kolekcija objekata klase `Karta'.")

        return 0

    @classmethod
    def vrijednostTable (cls):
        """
        Dohvati bodovnu vrijednost ostvarenja table.

        """

        return 1

    @classmethod
    def vrijednostMax (cls):
        """
        Dohvati bodovnu vrijednost strogo najvise skupljenih karata u partiji.

        """

        return 3

    @classmethod
    def moguciPotezi (cls, S):
        """
        Pronadi sve moguce sume karata u kolekciji karata S.

        Povratna vrijednost je dict ciji su kljucevi znakovi karata (objekti
        klase Karta.Znak), a vrijednosti objekti klase set elemenata objekata
        klase frozenset elemenata objekata klase Karta.  Svakom kljucu u
        povratnom rjecniku pridruzena je familija podskupova S cija suma u
        pravilima igre tablic daje (medu ostalim) taj znak.

        Ako neki znak nije kljuc povratnog rjecnika, nijedan podskup skupa S ne
        moze se sumirati u taj znak po pravilima igre tablic.

        """

        # Inicijaliziraj rjecnik poteza na prazni rjecnik.
        M = dict()

        # Izracunaj sve neprazne podskupove skupa S.
        P = partitivniSkup(S) - {frozenset()}

        # Izracunaj rjecnik poteza.
        for A in P:
            for x in sum(A):
                x = Karta.Znak(x if x != 11 else 1)
                if x in M:
                    M[x] |= {A}
                else:
                    M.update({x : {A}})

        # Vrati izracunati rjecnik poteza.
        return M

    def __new__ (cls, *args, **kwargs):
        """
        Kreiraj objekt klase Tablic.

        """

        return super(Tablic, cls).__new__(cls)

    def __init__ (self, spil = None):
        """
        Inicijaliziraj objekt klase Tablic.

        Ako je argument spil None, za spil koji se koristi u partiji generira
        se novi promijesani spil (52 karte) od povratne vrijednosti poziva
        funkcije
            >>> Karta.noviSpil()
        Inace taj argument mora biti iterabilni objekt svih objekata bez
        duplikata iz skupa povratne vrijednosti poziva funkcije
            >>> Karta.noviSpil()
        u bilo kojem poretku (u tom je onda poretku, dakle tako je promijesan,
        spil kojim ce se partija igrati).

        """

        if spil is None:
            # Generiraj novi promijesani spil karata.
            spil = list(Karta.noviSpil())
            random.shuffle(spil)

        self.__pokrenuta = False
        self.__zavrsena = False

        self.__spil = queue.Queue()
        for karta in spil:
            self.__spil.put(karta)

        self.__igraci = list()
        self.__stol = set()

    def __repr__ (self):
        """
        Dohvati repr(self).

        """

        return '<{0:s}: {{pokrenuta: {1:s}, zavrsena: {2:s}, igraci: ({3:s})}}>'.format(self.__class__.__name__, repr(self.__pokrenuta), repr(self.__zavrsena), str.join(', ', [repr(igrac['igrac']) for igrac in self.__igraci]))

    def __str__ (self):
        """
        Dohvati str(self).

        """

        return '{0:s}({1:s})'.format(self.__class__.__name__, str.join(', ', [str(igrac['igrac']) for igrac in self.__igraci]))

    def __unicode__ (self):
        """
        Dohvati unicode(self).

        """

        return unicode('{0:s}({1:s})').format(self.__class__.__name__, unicode.join(unicode(', '), [unicode(igrac['igrac']) for igrac in self.__igraci]))

    def dodajIgraca (self, klasa = RandomIgrac, *args, **kwargs):
        """
        Dodaj igraca (objekt klase klasa) u partiju.

        Argumenti *args, **kwargs prosljeduju se konstruktoru klase klasa pri
        inicijalizaciji novog dodanog igraca.  Ako postoji kljuc 'i' u rjecniku
        kwargs, ignorira se.

        """

        # Provjeri stanje partije.
        if self.__pokrenuta:
            raise RuntimeError('Nemoguce je dodati igraca u pokrenutu partiju.')

        # Dodaj novog igraca u partiju.
        kwargs.pop('i', None)
        self.__igraci.append({'igrac' : klasa(len(self.__igraci), *args, **kwargs),
                              'ruka' : set(),
                              'skupljeno' : set(),
                              'table' : 0,
                              'max' : False})

    def jePokrenuta (self):
        """
        Provjeri je li partija vec pokrenuta.

        """

        return self.__pokrenuta

    def jeZavrsena (self):
        """
        Provjeri je li partija vec zavrsena.

        """

        return self.__zavrsena

    def dohvatiBrojIgraca (self):
        """
        Dohvati trenutni broj igraca u partiji.

        """

        return len(self.__igraci)

    def dohvatiStol (self):
        """
        Dohvati trenutno stanje (sadrzaj) stola u partiji.

        """

        return copy.deepcopy(self.__stol)

    def dohvatiIgraca (self, i):
        """
        Dohvati igraca s indeksom i.

        Povratna vrijednost je objekt klase i-tog igraca ekvivalentan i-tom
        igracu u partiji.

        """

        return copy.deepcopy(self.__igraci[i]['igrac'])

    def hoceRazlog (self, i):
        """
        Provjeri zeli li i-ti igrac razlog eventualnog ponavljanja poteza.

        """

        return self.__igraci[i]['igrac'].hocuRazlog()

    def dohvatiIme (self, i):
        """
        Dohvati ime igraca s indeksom i.

        """

        return self.__igraci[i]['igrac'].dohvatiIme()

    def dohvatiSkupljeno (self, i):
        """
        Dohvati skup dosad skupljenih karata igraca s indeksom i.

        """

        return copy.deepcopy(self.__igraci[i]['skupljeno'])

    def dohvatiTable (self, i):
        """
        Dohvati broj dosad skupljenih tabli igraca s indeksom i.

        """

        return copy.deepcopy(self.__igraci[i]['table'])

    def dohvatiMax (self, i):
        """
        Saznaj je li igrac s indeksom i skupio strogo najvise karata.

        Ako partija jos nije zavrsila, povratna vrijednost bit ce False.  Ako
        je partija zavrsila, povratna vrijednost bit ce tuple kojemu je na
        indeksu 0 bool vrijednost koja je True ako i samo ako je igrac s
        indeksom i skupio strogo najvise karata, a na indeksu 1 broj skupljenih
        karata.

        """

        return copy.deepcopy(self.__igraci[i]['max'])

    def igraj (self, *logovi):
        """
        Odigraj brojPartija partija i poteze zapisi u zapisnike logovi.

        Objekt logovi mora biti tuple objekata podklase klase Tablic.Log.  Ako
        nije zadan nijedan zapisnik, povratna vrijednost funkcije je None.  Ako
        je zadan tocno jedan zapisnik, povratna vrijednost je taj zapisnik.
        Inace je povratna vrijednpst tuple zapisnika istim redom kojim su dani
        kao argumenti.

        Nakon pokretanja funkcije funkcija jePokrenuta vracat ce True, a nakon
        izvrsavanja funkcije funkcija jeZavrsena vracat ce True, a
        dohvatiMax vracat ce tuple koji odgovara je li igrac skupio strogo
        najvise karata i koliko je karata skupio.

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
            Zavrsi partiju.

            Vrijednost self.__zavrsena postavlja se na True, stol se ostatak
            karata na stolu daje se igracu s indeksom zadnji u skup skupljenih
            karata (ako zadnji nije None) i trazi se strogi maksimum skupljenih
            karata.

            """

            self.__zavrsena = True

            if not zadnji is None:
                # "Pocisti" stol.
                while self.__stol:
                    karta = self.__stol.pop()
                    self.__igraci[zadnji]['skupljeno'] |= {karta}

            # Pronadi igraca sa strogo najvise skupljenih karata ako postoji.
            I = [0]
            self.__igraci[0]['max'] = (False, len(self.__igraci[0]['skupljeno']))
            for j in range(1, len(self.__igraci)):
                self.__igraci[j]['max'] = (False, len(self.__igraci[j]['skupljeno']))
                if len(self.__igraci[j]['skupljeno']) > len(self.__igraci[I[0]]['skupljeno']):
                    I = [j]
                elif len(self.__igraci[j]['skupljeno']) == len(self.__igraci[I[0]]['skupljeno']):
                    I.append(j)

            if len(I) == 1:
                # Evaluiraj strogo najveci broja skupljenih karata.
                self.__igraci[I[0]]['max'] = (True, len(self.__igraci[I[0]]['skupljeno']))

        def __podijeli ():
            """
            Podijeli svim igracima jednak broj karata (sto vise, a najvise 6).

            Povratna vrijednost je broj karata podijeljenih svakom igracu.

            """

            for i in range(Tablic.inicijalniBrojKarata_ruka()):
                for j in range(len(self.__igraci)):
                    self.__igraci[j]['ruka'] |= {self.__spil.get()}
                if self.__spil.empty():
                    return i + 1

            return Tablic.inicijalniBrojKarata_ruka()

        def __objaviNovoDijeljenje (stol):
            """
            Pozovi Igrac.saznajNovoDijeljenje na svakom igracu.

            """

            for i in range(len(self.__igraci)):
                self.__igraci[i]['igrac'].saznajNovoDijeljenje(copy.deepcopy(self.__igraci[i]['ruka']), copy.deepcopy(stol))

        def __legalniPotez (i, karta, skupljeno, razlog = False):
            """
            Provjeri je li potez igraca s indeksom i legalan.

            Ako je razlog False, povratna vrijednost je bool vrijednosti True
            ako i samo ako je potez legalan.  Ako je razlog True, u slucaju
            ilegalnog poteza povratna vrijednost je tuple kojemu je na indeksu
            0 False, a na tuple s razlozima
                --  ako igrac s indeksom i u ruci nema kartu karta, tuple
                    razloga ce sadrzavati objekt karta,
                --  ako skup skupljeno nije podskup trenutnog skupa karata na
                    stolu, tuple razloga ce sadrzavati objekt skupljeno,
                --  ako ne postoji podskup skupa skupljeno koji se moze
                    sumirati u znak karte karta, tuple razloga ce sadrzavati
                    karta.znak,
                --  ako se skup karata skupljeno ne moze podijeliti na
                    particiju ciji se svaki clan moze sumirati u znak karte
                    karta, tuple razloga ce sadrzavati False.
            Sume karata racunaju se po pravilima igre tablic.

            """

            greske = list()

            # Provjeri je li karta u ruci.
            if not karta in self.__igraci[i]['ruka']:
                greske.append(karta)

            # Provjeri je li skupljeno na stolu.
            if not skupljeno <= self.__stol:
                greske.append(skupljeno)

            # Ako se skuplja sa stola, provjeri sume.
            if skupljeno:
                M = Tablic.moguciPotezi(skupljeno)
                if not karta.znak in M:
                    greske.append(karta.znak)
                else:
                    if not frozenset(skupljeno) in unijeDisjunktnih(M[karta.znak]):
                        greske.append(False)

            # Ako treba, vrati ilegalnost poteza i greske.
            if razlog and greske:
                return (False, tuple(greske))

            # Vrati legalnost poteza.
            return not greske

        def __dohvatiPotez (i):
            """
            Zovi Igrac.odigraj s na igracu i do prvog legalnog poteza.

            Povratna vrijednost je tuple (karta, skupljeno) tako da je i-ti
            igrac odigrao legalni potez igranja karte karta iz ruke i
            skupljanjem karata u skupu skupljeno sa stola (odnosno samo
            odlaganjem karte karta na stol ako i samo ako je skupljeno prazni
            skup).

            """

            # Inicijaliziraj ponovi i razlog na False, None respektivno.
            ponovi = False
            razlog = None

            while True:
                # Dohvati potez od igraca i provjeri njegovu legalnost.
                karta, skupljeno = self.__igraci[i]['igrac'].odigraj(copy.deepcopy(self.__igraci[i]['ruka']), copy.deepcopy(self.__stol), ponovi)
                legalno = __legalniPotez(i, karta, skupljeno, self.__igraci[i]['igrac'].hocuRazlog())
                if isinstance(legalno, tuple):
                    legalno, razlog = legalno

                # Ako je potez legalan, prekini petlju.  Inace postavi
                # vrijednost ponovi i udi u sljedecu iteraciju petlje.
                if legalno:
                    break
                elif razlog is None:
                    ponovi = True
                else:
                    ponovi = (True, razlog)

            # Vrati dohvaceni potez.
            return (karta, skupljeno)

        def __objaviPotez (i, karta, skupljeno):
            """
            Pozovi Igrac.vidiPotez na svakom igracu.

            """

            for j in range(len(self.__igraci)):
                self.__igraci[j]['igrac'].vidiPotez(i, copy.deepcopy(self.__igraci[j]['ruka']), copy.deepcopy(self.__stol), karta, copy.deepcopy(skupljeno))

        def __uzmiIzRuke (i, karta, skupi):
            """
            Makni kartu iz ruke igraca.

            Ako je skupi True, karta se stavlja u igracev skup skupljenih
            karata.  Inace se karta stavlja na stol.

            """

            self.__igraci[i]['ruka'].remove(karta)
            if skupi:
                self.__igraci[i]['skupljeno'] |= {karta}
            else:
                self.__stol |= {karta}

        def __uzmiSaStola (i, skupljeno):
            """
            Makni kartu sa stola i stavi ju u skup skupljenih karata igraca.

            """

            for karta in skupljeno:
                self.__stol.remove(karta)
                self.__igraci[i]['skupljeno'] |= {karta}

        def __provjeriTablu (i):
            """
            Ako je nakon igracevog poteza stol prazan, dodaj mu tablu.

            """

            if not self.__stol:
                self.__igraci[i]['table'] += 1

        def __objaviRezultat (rezultat):
            """
            Pozovi Igrac.saznajRezultat na svakom igracu.

            """

            for i in range(len(self.__igraci)):
                self.__igraci[i]['igrac'].saznajRezultat(copy.deepcopy(rezultat))

        logovi = list(logovi)

        # Provjeri stanje partije.

        if self.__pokrenuta:
            raise RuntimeError('Trenutna partija vec je pokrenuta.')

        if not self.__igraci:
            raise RuntimeError('Trenutna partija nema igraca.')

        if len(self.__igraci) == 1 or (52 - Tablic.inicijalniBrojKarata_stol()) % len(self.__igraci):
            raise RuntimeError('{0:d} nije valjani broj igraca u partiji igre tablic.'.format(len(self.__igraci)))

        # Pokreni partiju.
        __pokreni()

        # Logiraj i objavi pocetak nove partije.
        for i in range(len(logovi)):
            logovi[i].novaPartija(len(self.__igraci), [copy.deepcopy(self.__igraci[j]['igrac']) for j in range(len(self.__igraci))])
        __objaviBrojIgraca()

        # Igraj partiju.

        zadnji = None
        while not self.__spil.empty():
            # Podijeli karte i logiraj i objavi novo dijeljenje.
            k = __podijeli()
            for i in range(len(logovi)):
                logovi[i].novoDijeljenje(k, copy.deepcopy(self.__stol))
            __objaviNovoDijeljenje(self.__stol)

            while self.__igraci[0]['ruka']:
                for i in range(len(self.__igraci)):
                    # Dohvati, logiraj i objavi potez.
                    karta, skupljeno = __dohvatiPotez(i)
                    for j in range(len(logovi)):
                        logovi[j].logirajPotez(i,
                                               [copy.deepcopy(self.__igraci[k]['igrac']) for k in range(len(self.__igraci))],
                                               copy.deepcopy(self.__igraci[i]['ruka']), copy.deepcopy(self.__stol),
                                               karta, copy.deepcopy(skupljeno))
                    __objaviPotez(i, karta, skupljeno)

                    # Promijeni stanje igre ovisno o potezu.
                    __uzmiIzRuke(i, karta, bool(skupljeno))
                    if skupljeno:
                        __uzmiSaStola(i, skupljeno)
                        __provjeriTablu(i)
                        zadnji = i

        # Zavrsi partiju.
        __zavrsi(zadnji)
        rezultat = self.dohvatiRezultat()
        __objaviRezultat(rezultat)
        for i in range(len(logovi)):
            logovi[i].kraj(copy.deepcopy(rezultat))

        # Vrati odgovarajucu povratnu vrijednost.

        if not logovi:
            return None

        if len(logovi) == 1:
            return logovi[0]

        return tuple(logovi)

    def dohvatiRezultat (self):
        """
        Dohvati trenutne rezultate igraca.

        Povratna vrijednost je objekt klase list kojemu je na indeksu i zapisan
        rezultat igraca s indeksom i.  Svaki element povratne liste je objekt
        klase dict s kljucevima i vrijednostima
            --  'ime' : ime igraca,
            --  'skupljeno' : bodovna vrijednost skupa skupljenih karata,
            --  'table' : broj skupljenih tabli,
            --  'max' : je li skupio strogo najvise karata.

        """

        # Inicijaliziraj rezultat na praznu listu.
        rezultati = list()

        # Izracuinaj rezultat.
        for i in range(len(self.__igraci)):
            r = {'ime' : self.__igraci[i]['igrac'].dohvatiIme(),
                 'skupljeno' : 0,
                 'table' : self.__igraci[i]['table'],
                 'max' : self.__igraci[i]['max']}
            for karta in self.__igraci[i]['skupljeno']:
                r['skupljeno'] += Tablic.vrijednostKarata(karta)
            rezultati.append(r)

        # Vrati izracunati rezultat.
        return rezultati
