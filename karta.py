# -*- coding: utf-8 -*-

"""
Implementacija klase Karta za reprezentaciju karata u igri tablic.

"""

import copy
import enum
import math
import six

if six.PY3:
    unicode = str
    long = int

class Karta (object):
    """
    Klasa za reprezentaciju igracih karata.

    Klasa Karta optimizirana je za igru tablic.

    """

    @enum.unique
    class Boja (enum.IntEnum):
        """
        Enumeracija za reprezentaciju kartaskih boja (herc, pik, karo, tref).

        """

        NA = 0

        HERC = 1
        PIK  = 2
        KARO = 3
        TREF = 4

        @classmethod
        def postoji (cls, boja):
            """
            Provjeri postoji li boja enumeracijske vrijednosti `znak' (int ili
            float).

            """
            return any(boja == x for x in cls)

    @enum.unique
    class Znak (enum.IntEnum):
        """
        Enumeracija za reprezentaciju kartaskih znakova/simbola.

        Klasa Karta.Znak optimizirana je za igru tablic (enumeracijske
        vrijednosti simbola odgovaraju numerickim vrijednostima u igri tablic).

        """

        NA = 0

        A = 1

        BR2  = 2
        BR3  = 3
        BR4  = 4
        BR5  = 5
        BR6  = 6
        BR7  = 7
        BR8  = 8
        BR9  = 9
        BR10 = 10

        J = 12
        Q = 13
        K = 14

        @classmethod
        def postoji (cls, znak):
            """
            Provjeri postoji li znak enumeracijske vrijednosti `znak'.

            """

            return any(znak == x for x in cls)

    class __Iterator (object):
        """
        Klasa za iteratore za iteriranje po objektu klase Karta.

        """

        def __init__ (self, karta, i, stop, inkr):
            """
            Inicijaliziraj iterator za iteriranje po objektu karta.

            """

            self.__karta = karta

            self.__i = i
            self.__stop = stop
            self.__inkr = inkr

        def __copy__ (self):
            """
            Dohvati copy.copy(self).

            """

            return __Iterator(self.__karta, self.__i, self.__stop, self.__inkr)

        def __deepcopy__ (self, memodict = dict()):
            """
            Dohvati copy.deepcopy(self, memodict).

            """

            return __Iterator(copy.deepcopy(self.__karta, memodict),
                              copy.deepcopy(self.__i, memodict),
                              copy.deepcopy(self.__stop, memodict),
                              copy.deepcopy(self.__inkr, memodict))

        def __iter__ (self):
            """
            Dohvati iter(self).

            """

            return self

        def next (self):
            """
            Dohvati next(self).

            """

            if self.__inkr >= 0 and self.__i >= self.__stop or self.__inkr <= 0 and self.__i <= self.__stop:
                raise StopIteration()

            x = self.__karta[self.__i]
            self.__i += self.__inkr

            return x

        __next__ = next

    @classmethod
    def uKarte (cls, x):
        """
        Pretvori objekt x u objekt ili tuple objekata klase Karta.

        Ako je x nekakva kolekcija, pretvorba se vrsi rekurzivno, stoga je
        zapravo
            >>> x = (((1, 1), (2, 2), (3, 3)), (4, 4))
            >>> Karta.uKarte(x)
            ((<Karta: (<Boja.HERC: 1>, <Znak.A: 1>)>, <Karta: (<Boja.PIK: 2>, <Znak.BR2: 2>)>, <Karta: (<Boja.KARO: 3>, <Znak.BR3: 3>)>), <Karta: (<Boja.TREF: 4>, <Znak.BR4: 4>)>)

        """

        if hasattr(x, '__iter__'):
            try:
                return Karta(x)
            except (TypeError, ValueError):
                R = list()
                for y in x:
                    R.append(Karta.uKarte(y))
                return tuple(R)

        return Karta(x)

    @classmethod
    def noviSpil (cls):
        """
        Dohvati skup od 52 valjane igrace karte.

        """

        return {Karta(boja, znak) for boja in [Karta.Boja.HERC, Karta.Boja.PIK, Karta.Boja.KARO, Karta.Boja.TREF]
                                  for znak in [Karta.Znak.A, Karta.Znak.BR2, Karta.Znak.BR3, Karta.Znak.BR4, Karta.Znak.BR5, Karta.Znak.BR6, Karta.Znak.BR7, Karta.Znak.BR8, Karta.Znak.BR9, Karta.Znak.BR10, Karta.Znak.J, Karta.Znak.Q, Karta.Znak.K]}

    def __new__ (cls, *args, **kwargs):
        """
        Kreiraj objekt klase Karta.

        """

        return super(Karta, cls).__new__(cls)

    def __init__ (self, *args, **kwargs):
        """
        Inicijaliziraj objekt klase karta.

        Objekt klase Karta moze se inicijalizirati na vise nacina:
            1.  s 0 argumenata
                    >>> Karta()
                    <Karta: (<Boja.NA: 0>, <Znak.NA: 0>)>
            2.  s 1 argumentom objektom klase Karta
                    >>> Karta(Karta(boja = 'karo', znak = 10))
                    <Karta: (<Boja.KARO: 3>, <Znak.BR10: 10>)>
            3.  s 1 argumentom objektom klase Karta.Boja ili Karta.Znak
                    >>> Karta(Karta.Boja.KARO)
                    <Karta: (<Boja.KARO: 3>, <Znak.NA: 0>)>
                    >>> Karta(Karta.Znak.BR10)
                    <Karta: (<Boja.NA: 0>, <Znak.BR10: 10>)>
            4.  s 1 argumentom None
                    >>> Karta(None)
                    <Karta: (<Boja.NA: 0>, <Znak.NA: 0>)>
            5.  s 1 argumentom objektom klase str ili unicode
                    >>> Karta('herc')
                    <Karta: (<Boja.HERC: 1>, <Znak.NA: 0>)>
                    >>> Karta('10')
                    <Karta: (<Boja.NA: 0>, <Znak.BR10: 10>)>
                    >>> Karta('herc 10')
                    <Karta: (<Boja.HERC: 1>, <Znak.BR10: 10>)>
                    >>> Karta('herc10')
                    <Karta: (<Boja.HERC: 1>, <Znak.BR10: 10>)>
            6.  s 1 argumentom objektom klase int, long, float ili complex
                    >>> Karta(10)
                    <Karta: (<Boja.NA: 0>, <Znak.BR10: 10>)>
            7.  s 1 argumentom rjecnikom ciji su kljucevi u skupu
                {'boja', 'znak'}, a vrijednosti objekti klase int, long, float,
                complex, str, unicode ili odgovarajuce enumeracije (Karta.Boja
                odnosno Karta.Znak)
                    >>> Karta({'boja' : 'karo', 'znak' : 10})
                    <Karta: (<Boja.KARO: 3>, <Znak.BR10: 10>)>
            8.  s 1 argumentom iterabilnim objektom od dva elementa objekta
                klase int, long, float, complex, str, unicode ili odgovarajuce
                enumeracije (Karta.Boja odnosno Karta.Znak)
                    >>> Karta(('karo', 10))
                    <Karta: (<Boja.KARO: 3>, <Znak.NA: 0>)>
            9.  s 2 argumenta objekta None ili klase int, long, float, complex,
                str, unicode ili odgovarajuce enumeracije (Karta.Boja odnosno
                Karta.Znak)
                    >>> Karta('karo', 10)
                    <Karta: (<Boja.KARO: 3>, <Znak.BR10: 10>)>
            10. s argumentima zadanim kljucnim rijecima iz skupa
                {'boja', 'znak'} objektima None ili klase int, long, float,
                complex, str, unicode ili odgovarajuce enumeracije (Karta.Boja
                odnosno Karta.Znak)
                    >>> Karta(boja = 'karo', znak = 10)
                    <Karta: (<Boja.KARO: 3>, <Znak.BR10: 10>)>
        Ako je neka zadana vrijednost objekt klase complex, njezin imaginarni
        dio mora biti jednak 0 i tada se ta vrijednost tretira kao vrijednost
        njezinog realnog dijela.  Ako je neka zadana vrijednost objekt klase
        int ili float, odgovarajuci atribut postavlja se na odgovarajuci
        enumeracijsku konstantu cija je enumeracijska vrijednost taj broj.  Ako
        je neka zadana vrijednost objekt klase str ili unicode, odgovarajuci
        atribut postavlja se na odgovarajuci enumeracijsku konstantu cije je
        ime taj string.  Ako je znak zadan brojem 11, znak se postavlja na A
        (Karta(znak = 1) i Karta(znak = 11) inicijaliziraju istu kartu).  Imena
        boja ne moraju biti zadana potpuno (Karta('h'), Karta('he'),
        Karta('her') i Karta('herc') inicijaliziraju istu kartu), ali imena
        znakova moraju.  Kljucevi rjecnika odnosno kljucne rijeci su
        case-sensitive (moraju biti zadani malim slovima), ali vrijednosti nisu
        (Karta(boja = 'karo') i Karta(boja = 'KARO') inicijaliziraju istu
        kartu).

        Moguce iznimke su klase TypeError, a izbacuju se ako
            1.  su argumenti zadani implicitno i eksplicitno (kljucnim
                rijecima), kao na primjer Karta(10, boja = 'karo'),
            2.  je zadan argument rjecnik s kljucevima koji nisu u skupu
                {'boja', 'znak'},
            3.  je zadan 1 argument koji nije None ni objekt klase int, float,
                complex, str, unicode ili dict i nije iterabilan,
            4.  je zadan 1 iterabilni argument ciji je broj elemenata razlicit
                od 2,
            5.  je zadano strogo vise od 2 argumenta,
            6.  su zadani argumenti kljucnim rijecima koje nisu u skupu
                {'boja', 'znak'}.
        Takoder, iznimke za konverziju objekata u enumeracije Karta.Boja i
        Karta.Znak ne saniraju se, stoga i one mogu biti izbacene.

        """

        # Inicijalizacija karte na nedefiniranu kartu.
        self.boja = Karta.Boja.NA
        self.znak = Karta.Znak.NA

        # Citanje argumenata.
        if args:
            # Citanje implicitno zadanih argumenata.
            if kwargs:
                # Nije dopusteno implicitno i eksplicitno zadavanje argumenata.
                raise TypeError("Argumenti za inicijalizaciju objekta klase `Karta' moraju biti zadani implicitno ili eksplicitno (kljucnim rijecima), a ne na oba nacina.")
            if len(args) == 1:
                # Citanje samo 1 argumenta.
                if args[0] is None:
                    pass
                elif isinstance(args[0], Karta):
                    # Kreiranje kopije karte.
                    self.boja = args[0].boja
                    self.znak = args[0].znak
                elif isinstance(args[0], Karta.Boja):
                    # Zadavanje samo boje karte.
                    self.boja = args[0]
                elif isinstance(args[0], (int, long, float, complex, Karta.Znak)):
                    # Zadavanje samo znaka karte.
                    self.znak = args[0]
                elif isinstance(args[0], (str, unicode)):
                    # Zadavanje karte stringom.
                    if args[0].upper() in Karta.Boja.__members__:
                        self.boja = args[0]
                    else:
                        # Rastavljanje stringa.
                        karta = args[0].split()
                        if len(karta) == 1:
                            # Ako je string i nakon rastavljanja jedinstven,
                            # rastavlja se rucno.
                            stop = False
                            for j in range(len(karta[0])):
                                if karta[0][j].isdigit() or karta[0][j:].upper() in Karta.Znak.__members__:
                                    stop = True

                                    break
                            if not stop:
                                j = len(karta[0])

                            if j:
                                # Prvi dio stringa zadaje boju.
                                self.boja = karta[0][:j]
                            if j < len(karta[0]):
                                # Drugi dio stringa zadaje znak.
                                self.znak = karta[0][j:]
                        elif len(karta) == 2:
                            # Prvi dio stringa zadaje boju, a drugi znak.
                            self.boja = karta[0]
                            self.znak = karta[1]
                        elif karta:
                            # Rastav stringa na st(self.__inkr <= 0 or self.__i >= self.__stop) and (self.__inkr >= 0 or self.__i <= self.__stop):rogo vise od 2 podstringa se ne prepoznaje.
                            raise TypeError("String `{0:s}' nije valjani argument za inicijalizaciju objekta klase Karta.".format(args[0]))
                elif isinstance(args[0], dict):
                    # Zadavanje karte rjecnikom.
                    if not set(args[0].keys()) <= {'boja', 'znak'}:
                        raise TypeError("Za inicijalizaciju objekta klase `Karta' dan je argument rjcnik s nepoznatim kljucevima.")
                    if 'boja' in args[0]:
                        self.boja = args[0]['boja']
                    if 'znak' in args[0]:
                        self.znak = args[0]['znak']
                else:
                    # Zadavanje karte iterabilnim objektom.
                    try:
                        karta = tuple(args[0])
                    except (TypeError, ValueError):
                        raise TypeError("Argument {0} nije valjani argument za inicijalizaciju objekta klase `Karta'.".format(args[0]))
                    else:
                        if len(karta) == 2:
                            self.boja = karta[0]
                            self.znak = karta[1]
                        else:
                            # Iterabilni objekt koji nema tocno 2 elementa se ne prepoznaje.
                            raise TypeError("Tuple {0} nije valjani argument za inicijalizaciju objekta klase `Karta'.".format(args[0]))
            elif len(args) == 2:
                # Citanje dvaju argumenata.
                self.boja = args[0]
                self.znak = args[1]
            else:
                # Zadavanje karte sa strogo vise od 2 argumenta se ne prepoznaje.
                raise TypeError("Zadano je previse argumenata za inicijalizaciju objekta klase `Karta'.")
        if kwargs:
            # Citanje eksplicitno zadanih argumenata.
            if args:
                # Nije dopusteno implicitno i eksplicitno zadavanje argumenata.
                raise TypeError("Argumenti za inicijalizaciju objekta klase `Karta' moraju biti zadani implicitno ili eksplicitno (kljucnim rijecima), a ne na oba nacina.")
            if not set(kwargs.keys()) <= {'boja', 'znak'}:
                raise TypeError("Za inicijalizaciju objekta klase `Karta' zadane su nepoznate kljucne rijeci.")
            if 'boja' in kwargs:
                self.boja = kwargs['boja']
            if 'znak' in kwargs:
                self.znak = kwargs['znak']

    def __getattr__ (self, name):
        """
        Pokusaj dohvatiti nepostojeci atribut.

        """

        raise AttributeError("Atribut `{0:s}' ne postoji.".format(name))

    def __setattr__ (self, name, value):
        """
        Pokusaj zadati vrijednost atributa.

        Ako atribut name ne postoji, izbacuje se iznimka tipa AttributeError.

        U daljnjem tekstu enumeracija je Karta.Boja ako je name = 'boja' odnosno
        Karta.Znak ako je name = 'znak'.  Ako je value objekt klase enumeracija,
        vrijednost atributa name postavlja se na value.

        Ako je value None, atribut name postavlja se na enumeracija.NA.  Ako je
        value objekt klase complex i ako je value.imag != 0, izbacuje se iznimka
        tipa ValueError; inace se uzima value = float(value.real).
        Ako je value objekt klase int, long ili float i vrijedi
            >>> enumeracija.postoji(value)
            False
        izbacuje se iznimka tipa ValueError osim ako je vrijednost nan (u tom se
        slucaju uzima enumeracija.NA) ili ako je enueracija Karta.Znak i
        value = 11 (u tom se slucaju uzima value = 1); inace se atribut name
        postavlja na
            >>> enumeracija(value)
        Ako je value objekt klase str ili unicode, pokusava se (ako neki korak
        uspije, sljedeci se ne izvrsavaju ni ne pokusavaju) redom
            1.  ako je value = 'None', vrijednost atributa name postavlja se na
                enueracija.NA,
            2.  value = int(value),
            3.  value = long(value),
            4.  value = float(value),
            5.  value = complex(value),
            6.  vrijednost atributa name postavlja se na enueracija.NA ako je
                value = '',
            7.  ako je enumeracija Karta.BOJA, vrijednost atributa name
                postavlja se na vrijednost Karta.BOJA cije ime pocinje s
                value.upper(),
            8.  vrijednost atributa name postavlja se na
                enueracija[value.upper()].
        Ako uspije konverzija iz koraka 1. -- 4., daljnji je postupak jednak kao
        da je vrijednost value odmah bila zadana kao numericka vrijednost
        odgovarajuceg tipa.  Ako nijedan korak ne uspije, izbacuje se iznimka
        tipa ValueError.

        Ako value nije None ni objekt klase enumeracija, int, long, float,
        complex, str ni unicode, izbacuje se iznimka tipa TypeError.

        """

        def __prevedi (enumeracija, vrijednost):
            """
            Prevedi vrijednost u objekt klase enumeracija.

            """

            if vrijednost is None:
                return enumeracija.NA
            elif isinstance(vrijednost, enumeracija):
                # Ako prevodenje nije potrebno, vrati vrijednost.
                return vrijednost
            elif isinstance(vrijednost, (int, long, float)):
                # Prevodenje numericke vrijednosti.
                if math.isinf(vrijednost):
                    raise ValueError('Vrijednost {0} nije konacna.'.format(vrijednost))
                if math.isnan(vrijednost):
                    return enumeracija.NA
                if enumeracija is Karta.Znak and vrijednost == 11:
                    vrijednost = 1
                if enumeracija.postoji(vrijednost):
                    return enumeracija(vrijednost)

                raise ValueError('Vrijednost {0} nije valjani argument zadavanja atributa enumeracije {1:s}.'.format(vrijednost, enumeracija.__name__))
            elif isinstance(vrijednost, complex):
                if vrijednost.imag:
                    raise ValueError('Imaginarni dio vrijednosti {0} nije jednak 0.'.format(vrijednost))

                return __prevedi(enumeracija, float(vrijednost.real))
            elif isinstance(vrijednost, (str, unicode)):
                # Prevodenje stringa svodi se na pokusaj prevodenja stringa u
                # numericku vrijednost pa u objekt klase enumeracija, a, tek
                # ako to ne uspije, vrijednost se prevodi direktno.
                if vrijednost == 'None':
                    return enumeracija.NA
                try:
                    return __prevedi(enumeracija, int(vrijednost))
                except (TypeError, ValueError):
                    try:
                        return __prevedi(enumeracija, long(vrijednost))
                    except (TypeError, ValueError):
                        try:
                            return __prevedi(enumeracija, float(vrijednost))
                        except (TypeError, ValueError):
                            try:
                                return __prevedi(enumeracija, complex(vrijednost))
                            except (TypeError, ValueError):
                                pass
                if not vrijednost:
                    return enumeracija.NA
                elif enumeracija is Karta.Boja:
                    for x in enumeracija:
                        if len(vrijednost) > len(x.name):
                            continue
                        if vrijednost.upper() == x.name[0:len(vrijednost)]:
                            return x
                elif vrijednost.upper() in enumeracija.__members__:
                    return enumeracija[vrijednost.upper()]

                raise ValueError("Vrijednost `{0:s}' nije valjani argument zadavanja atributa enumeracije {1:s}.".format(vrijednost, enumeracija.__name__))

            raise TypeError("Vrijednost `{0:s}' nije valjana vrijednost za zadavanje enumeracije `{0:s}'.".format(repr(vrijednost), enumeracija.__name__))

        if name == 'boja':
            if 'boja' in self.__dict__:
                self.__dict__['boja'] = __prevedi(Karta.Boja, value)
            else:
                self.__dict__.update({'boja' : __prevedi(Karta.Boja, value)})
        elif name == 'znak':
            if 'znak' in self.__dict__:
                self.__dict__['znak'] = __prevedi(Karta.Znak, value)
            else:
                self.__dict__.update({'znak' : __prevedi(Karta.Znak, value)})
        else:
            raise AttributeError("Atribut `{0:s}' ne postoji.".format(name))

    def __delattr__ (self, name):
        """
        Pokusaj izbrisati atribut.

        """

        if name in {'boja', 'znak'}:
            raise TypeError("Atributi objekta klase `Karta' se ne mogu brisati.")

        raise AttributeError("Atribut `{0:s}' ne postoji".format(name))

    def __copy__ (self):
        """
        Dohvati copy.copy(self).

        """

        return Karta(self.boja, self.znak)

    def __deepcopy__ (self, memodict = dict()):
        """
        Dohvati copy.deepcopy(self, memodict).

        """

        return Karta(copy.deepcopy(self.boja, memodict), copy.deepcopy(self.znak, memodict))

    def __len__ (self):
        """
        Dohvati len(self).

        """

        return 2

    def __iter__ (self):
        """
        Iteriraj po karti.

        """

        return Karta.__Iterator(self, *slice(None, None, 1).indices(len(self)))

    def __reversed__ (self):
        """
        Iteriraj po karti u obrnutom redoslijedu.

        """

        return Karta.__Iterator(self, *slice(None, None, -1).indices(len(self)))

    def __getitem__ (self, key):
        """
        Pokusaj dohvatiti element.

        """

        if isinstance(key, slice):
            # Tretiranje specijalnog slucaja kada se dohvaca slice.
            return tuple(Karta.__Iterator(self, *key.indices(len(self))))

        if key == 0 or key == 'boja':
            return self.boja
        if key == 1 or key == 'znak':
            return self.znak

        raise KeyError("Kljuc key nije prepoznat.")

    def __setitem__ (self, key, value):
        """
        Pokusaj zadati element.

        """

        if isinstance(key, slice):
            # Tretiranje specijalnog slucaja kada se zadaje na slice-u.
            for i in range(*key.indices(len(self))):
                self.__setitem__(i, value)
            return

        if key == 0 or key == 'boja':
            self.boja = value
            return
        if key == 1 or key == 'znak':
            self.znak = value
            return

        raise KeyError("Kljuc key nije prepoznat.")

    def __delitem__ (self, key):
        """
        Pokusaj izbrisati element.

        """

        if key in {0, 'boja', 1, 'znak'} or isinstance(key, slice):
            raise TypeError("Elementi objekta klase `Karta' ne mogu se brisati.")

        raise KeyError("Kljuc key nije prepoznat.")

    def __contains__ (self, key):
        """
        Provjeri postoji li element.

        """

        return key in {0, 'boja', 1, 'znak'}

    def __add__ (self, value):
        """
        Zbroji trenutnu kartu i vrijednost value.

        Ako je value None, povratna vrijednost je skup koji sadrzi numericku
        vrijednost znaka karte ako karta nije nedefiniranog znaka odnosno
        prazni skup inace.  Ako je value nekakva kolekcija, zbrajanje se vrsi
        rekurzivno po njezinim elementima.  Ako je value objekt tipa int, long,
        float, str, unicode, Karta ili Karta.Znak, prevodi se u objekt tipa int
        direktno pretvorbom u numericku vrijednost, a ako za stringove ta
        pretvorba ne uspijeva, pokusava se pretvoriti u numericku vrijednost
        preko enumeracije Karta.Znak (ako ni to ne uspije, uzima se
        nedefinirani znak).  Povratna vrijednost je objekt tipa set ciji su
        elementi sve moguce sume karte i value.

        """

        if value is None:
            # Tretiranje specijalnog slucaja kada je value None.
            if self.znak is Karta.Znak.NA:
                return set()
            else:
                return {self.znak.value}

        if hasattr(value, '__iter__') and not isinstance(value, (str, unicode, Karta)):
            # Tretiranje specijalnog slucaja kada je value iterabilni objekt i
            # nije string ili objekt klase Karta.
            S = set()
            for y in value:
                S |= self.__add__(y)

            return S

        if isinstance(value, complex):
            if value.imag:
                raise ValueError('Imaginarni dio vrijednosti {0} nije jednak  0.'.format(value))
            value = float(value.real)

        if isinstance(value, int):
            if not Karta.Znak.postoji(value) and value != 11:
                raise ValueError('value mora biti 0, 11 ili numericka vrijednost neke karte.')
        else:
            try:
                value = int(Karta(value))
            except TypeError:
                raise TypeError("value mora biti objekt klase `int'.".format(repr(value)))
            except ValueError:
                raise ValueError("Vrijednost `{0:s}' nije valjani sumand za zbrajanje objekata klase `Karta'.".format(repr(value)))

        if self.znak is Karta.Znak.A and value == 1:
            # Tretiranje specijalnog slucaja zbrajanje 2 A.
            return {Karta.Znak.BR2.value, Karta.Znak.J.value}
        if self.znak is Karta.Znak.A:
            # Tretiranje specijalnog slucaja kada je karta znaka A.
            if 1 + value > 14:
                return set()
            if 11 + value > 14:
                return {1 + value}
            return {1 + value, 11 + value}
        if value == 1:
            # Tretiranje specijalnog slucaja kada je value A.
            if self.znak + 1 > 14:
                return set()
            if self.znak + 11 > 14:
                return {self.znak + 1}
            else:
                return {self.znak + 1, self.znak + 11}

        if self.znak + value > 14:
            # Ako je zbroj preveliki, zbroj nije moguc pa je povratna
            # vrijednost prazni skup.
            return set()

        # Vracanje skupa koji sadrzi jedinstvenu mogucu vrijednost zbroja.
        return {self.znak + value}

    def __radd__ (self, value):
        """
        Zbroji vrijednost value i trenutnu kartu.

        Zbrajanje karata je u tablicu komutativno stoga se za value + self
        vraca self.__add__(value).

        """

        return self.__add__(value)

    def __mul__ (self, value):
        """
        Pomnozi trenutnu kartu i cijeli broj.

        Mnozenje se vrsi uzastopnim zbrajanjem, stoga je mnozenje strogo
        negativnim brojem nedefinirano (izbacuje se iznimka tipa ValueError).
        Inace je za value == 0 povratna vrijednost 0, za 1 {self.znak.value}
        ako je self.znak != Karta.Znak.NA odnosno {} za
        self.znak == Karta.Znak.NA i self + self + ... + self (value istih
        sumanada) za value > 1.

        """

        if isinstance(value, complex):
            if value.imag:
                raise ValueError('Imaginarni dio vrijednosti {0} nije jednak 0.'.format(value))
            value = float(value.real)

        if isinstance(value, float):
            if math.isinf(value) or math.isnan(value):
                raise ValueError('value mora biti konacna vrijednost.')
        if not isinstance(value, int):
            try:
                value = int(value)
            except (TypeError, ValueError):
                try:
                    value = int(long(value))
                except (TypeError, ValueError):
                    try:
                        value = int(float(value))
                    except (TypeError, ValueError):
                        try:
                            return self.__mul__(complex(value))
                        except (TypeError, ValueError):
                            raise TypeError("value mora biti objekt klase `int'.")


        if value < 0:
            raise ValueError('value mora biti nenegativna vrijednost.')

        if not value:
            return set()

        rezultat = None
        while value:
            rezultat = self.__add__(rezultat)
            value -= 1

        return rezultat

    def __rmul__ (self, value):
        """
        Pomnozi cijeli broj i trenutnu kartu.

        Za value * self se vraca self.__mul__(value).

        """
        return self.__mul__(value)

    def __nonzero__ (self):
        """
        Dohvati bool(self).

        """

        return bool(self.boja.value and self.znak.value)

    __bool__ = __nonzero__

    def __int__ (self):
        """
        Dohvati int(self).

        """

        return int(self.znak.value)

    def __long__ (self):
        """
        Dohvati long(self).

        """

        return long(self.znak.value)

    def __oct__ (self):
        """
        Dohvati oct(self).

        """

        return oct(self.znak.value)

    def __hex__ (self):
        """
        Dohvati hex(self).

        """

        return hex(self.znak.value)

    def __float__ (self):
        """
        Dohvati float(self).

        """

        return float(self.znak.value)

    def __complex__ (self):
        """
        Dohvati complex(self).

        """

        return complex(self.znak.value)

    def __repr__ (self):
        """
        Dohvati repr(self).

        """

        return str('<{0:s}: ({1:s}, {2:s})>'.format(self.__class__.__name__, repr(self.boja), repr(self.znak)))

    def __str__ (self):
        """
        Dohvati str(self).

        """

        return str('{0:s}({1:s}, {2:s})'.format(self.__class__.__name__, str(self.boja), str(self.znak)))

    def __unicode__ (self):
        """
        Dohvati unicode(self).

        """

        return unicode('{0:s}({1:s}, {2:s})'.format(self.__class__.__name__, unicode(self.boja), unicode(self.znak)))

    def __coerce__ (self, other):
        """
        Svedi self i other na objekte istog tipa.

        Prvo se pokusava other konvertirati u objekt klase Karta, a, ako ta
        konverzija ne uspije, self se pokusava konvertirati u objekt klase koje
        je other.  Ako i ta konverzija ne uspije (rezultira iznimkom tipa
        TypeError, AttributeError ili ValueError), vraca se None.

        """

        try:
            return (self, Karta(other))
        except (TypeError, AttributeError, ValueError):
            try:
                return (type(other)(self), other)
            except (TypeError, AttributeError, ValueError):
                pass

        return None

    def __hash__ (self):
        """
        Dohvati hash(self).

        """

        return (self.boja.value + self.znak.value * len(list(Karta.Boja)))

    def __eq__ (self, value):
        """
        Usporedi (==) karte kao uredene parove boje i znaka.

        """

        if not isinstance(value, Karta):
            value = Karta(value)

        return self.znak == value.znak and self.boja == value.boja

    def __ne__ (self, value):
        """
        Usporedi (!=) karte kao uredene parove boje i znaka.

        """

        return not self.__eq__(value)

    def __lt__ (self, value):
        """
        Usporedi (<) karte antileksikografski kao uredene parove boje i znaka.

        """

        if not isinstance(value, Karta):
            value = Karta(value)

        return self.znak < value.znak or self.znak == value.znak and self.boja < value.boja

    def __gt__ (self, value):
        """
        Usporedi (>) karte antileksikografski kao uredene parove boje i znaka.

        """

        if not isinstance(value, Karta):
            value = Karta(value)

        return value.__lt__(self)

    def __le__ (self, value):
        """
        Usporedi (<=) karte antileksikografski kao uredene parove boje i znaka.

        """

        return not self.__gt__(value)

    def __ge__ (self, value):
        """
        Usporedi (>=) karte antileksikografski kao uredene parove boje i znaka.

        """

        return not self.__lt__(value)
