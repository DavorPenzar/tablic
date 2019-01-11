# -*- coding: utf-8 -*-

"""
Implementacija klase IOIgrac za stdin/stdout igraca igre tablic.

"""

import copy
import math
import six

from skupovi import partitivniSkup, unijeDisjunktnih
from karta import Karta
from engine import Tablic
from pohlepni_igrac import PohlepniIgrac

if six.PY3:
    unicode = str

class IOIgrac (Tablic.Igrac):
    """
    Klasa za stdin/stdout igraca igre tablic.

    """

    @classmethod
    def lijepiString (cls, x):
        """
        Dohvati "lijepi string" objekta x.

        Ako je x objekt klase Karta.Boja, vraca se string formata '??'' ako je
        boja nedefinirana (Karta.Boja.NA), a inace naziv boje malim slovima.
        Ako je x objekt klase Karta.Znak, vraca se string '??' ako je znak
        nedefiniran (Karta.Znak.NA), a inace 'A' za A, broj za kartu broja i
        'J', 'Q', 'K' za J, Q, K respektivno.  Ako je x objekt klase Karta,
        vraca se string formata '[boja] [znak]', gdje je '[boja]' "lijepi
        string" boje karte, a '[znak]' lijepi string znaka karte.  Ako se x
        moze pretvoriti u objekt klase Karta, vraca se "lijepi string" karte u
        koju se pretvara.  Ako je x kolekcija, vraca se string formata
        '[' + "lijepi stringovi" elemenata razmaknuti stringom ', ' + ']'.
        Inace se vraca str(x).

        """

        # Tretiraj specijalne slucajeve da je x kartaska boja, kartaski znak
        # ili karta.
        if isinstance(x, Karta.Boja):
            return '??' if x is Karta.Boja.NA else x.name.lower()
        if isinstance(x, Karta.Znak):
            if x is Karta.Znak.NA:
                return '??'
            elif x.value >= 2 and x.value <= 10:
                return str(x.value)

            return x.name
        if isinstance(x, Karta):
            return '{0:s} {1:s}'.format(IOIgrac.lijepiString(x.boja),
                                        IOIgrac.lijepiString(x.znak))

#       try:
#           return IOIgrac.lijepiString(Karta(x))
#       except (TypeError, ValueError):
#           pass

        # Tretiraj specijalne slucajeve da je x dict ili netekstualni iterabilni objekt.
        if isinstance(x, dict):
            return '{{{0:s}}}'.format(', '.join({0:s} : {1:s}'.format(IOIgrac.lijepiString(y), IOIgrac.lijepiString(z)) for y, z in six.iteritems(x)))
        elif hasattr(x, '__iter__') and not isinstance(x, (str, unicode)):
            return '[{0:s}]'.format(', '.join(IOIgrac.lijepiString(y) for y in x))

        # Vrati str(x).
        return str(x)

    def __init__ (self, i, ime = None):
        """
        Inicijaliziraj objekt klase IOIgrac.

        """

        Tablic.Igrac.__init__(self, i, ime)

        # Inicijaliziraj relevantne varijable

        self.__k = None # broj karata u spilu
        self.__n = None # broj igraca
        self.__imena = None # imena igraca

    def __copy__ (self):
        igrac = Tablic.Igrac.__copy__(self)

        igrac.__k = self.__k
        igrac.__n = self.__n
        igrac.__imena = self.__imena

        return igrac

    def __deepcopy__ (self, memodict = dict()):
        igrac = Tablic.Igrac.__deepcopy__(self, memodict)

        igrac.__k = copy.deepcopy(self.__k, memodict)
        igrac.__n = copy.deepcopy(self.__n, memodict)
        igrac.__imena = copy.deepcopy(self.__imena, memodict)

        return igrac

    def hocuRazlog (self):
        """
        Vrati True (stdin/stdout igrac zeli znati razlog ilegalnog poteza).

        """

        return True

    def saznajBrojIgraca (self, n, imena):
        """
        Ispisi na stdout koliko igraca je u partiji i ispisi njihova imena.

        """

        # Postavi pocetne vrijednosti relevantnih varijabli.
        self.__k = 52 - Tablic.inicijalniBrojKarata_stol()
        self.__n = n
        self.__imena = imena

        # Ispisi pocetak partije.
        print("Partija za {0:d} igraca:".format(self.__n))
        for i in range(self.__n):
            print("\t{0:d}.\t{1:s}{2:s}".format(i + 1, self.__imena[i], ' (*)' if i == self.dohvatiIndeks() else ''))
        print("\n")

    def saznajNovoDijeljenje (self, ruka, stol):
        """
        Ispisi na stdout kako izgledaju stol i ruka nakon novog dijeljenja.

        """

        # Izracunaj ukupni broj dijeljenja u partiji.
        ukupno = int(math.ceil(float(52 - Tablic.inicijalniBrojKarata_stol()) / (self.__n * Tablic.inicijalniBrojKarata_ruka())))

        # Azuriraj broj karata u spilu.
        self.__k -= self.__n * len(ruka)

        # Ispisi novo dijeljenje.
        print('Dijeljenje {0:d}/{1:d}.'.format(ukupno - int(math.ceil(float(self.__k) / (self.__n * Tablic.inicijalniBrojKarata_ruka()))), ukupno))
        print('Na stolu:')
        print("\t{0:s}".format(IOIgrac.lijepiString(sorted(list(stol), reverse = True))))
        print('U ruci:')
        print("\t{0:s}\n".format(IOIgrac.lijepiString(sorted(list(ruka), reverse = True))))

    def vidiPotez (self, i, ruka, stol, karta, skupljeno):
        """
        Ispisi potez na stdout.

        """

        # Ako je trenutni igrac na potezu, ne ispisi potez (izadi iz funkcije).
        if i == self.dohvatiIndeks():
            return

        # Ispisi potez na stdout.
        print('{0:s} igra.'.format(self.__imena[i]))
        print('Na stolu:')
        print("\t{0:s}".format(IOIgrac.lijepiString(sorted(list(stol), reverse = True))))
        print('Potez:')
        print("\t{0:s} {1:s} {2:s}\n".format(IOIgrac.lijepiString(karta), '<' if skupljeno else '>', IOIgrac.lijepiString(sorted(list(skupljeno), reverse = True))))

    def saznajRezultat (self, rezultat):
        """
        Ispisi rezultat na stdout.

        """

        # Dohvati konacni rezultat.
        konacni_rezultat = Tablic.Log.konacniRezultat(rezultat)

        # Ispisi rezultat.
        print('Rezultat:')
        for i in range(self.__n):
            print("\t{0:s}{1:s}:".format(rezultat[i]['ime'], ' (*)' if i == self.dohvatiIndeks() else ''))
            print("\t\tBodovi: {0:d}".format(rezultat[i]['skupljeno']))
            print("\t\tTable: {0:d}".format(rezultat[i]['table']))
            print("\t\tBroj karata: {0:d}{1:s}".format(rezultat[i]['max'][1], ' [+]' if rezultat[i]['max'][0] else ''))
            print("\t\tUkupno: {0:d}".format(konacni_rezultat[i]))

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
            print("\t{0:s}{1:s}".format(rezultat[p]['ime'], ' (*)' if p == self.dohvatiIndeks() else ''))

    def odigraj (self, ruka, stol, ponovi = False):
        """
        Ucitaj potez sa stdin.

        Karte se mogu pisati implicitno, zadavajuci samo znak karte, ili
        eksplicitno.  Pri zadavanju skupa karata za skupiti moze se napisati
        'AUTO' (case-insensitive) pri cemu se uzima po pohlepnom algoritmu
        najpovoljniji potez kojim se skupljaju, medu ostalim, sve vec zadane
        karte za skupiti.  Inace se zavrsetak karata za skupiti zadaje praznim
        unosom.

        """

        # Ako treba, ispisi razlog ponavljanja poteza.  Inace javi da je igrac na redu.
        if isinstance(ponovi, tuple):
            ponovi, razlog = ponovi
        if ponovi:
            greske = list()
            for greska in razlog:
                if isinstance(greska, Karta):
                    greske.append('Karta {0:s} nije u ruci.'.format(IOIgrac.lijepiString(greska)))
                elif isinstance(greska, set):
                    greske.append('Skup karata {0:s} nije podskup skupa karata na stolu.'.format(IOIgrac.lijepiString(sorted(list(greska), reverse = True))))
                elif isinstance(greska, Karta.Znak):
                    greske.append('Znak {0:s} ne moze se dobiti sumiranjem nekih od skupljenih karata.'.format(IOIgrac.lijepiString(greska)))
                elif greska == False:
                    greske.append('Skupljene karte ne mogu se particionirati na skupove odgovarajucih suma.')
            print('  '.join(greske))
            print('Igraj ponovo!')
        else:
            print('Tvoj je red.')

        # Ispisi trenutno stanje stola i ruke.
        print('Na stolu:')
        print("\t{0:s}".format(IOIgrac.lijepiString(sorted(list(stol), reverse = True))))
        print('U ruci:')
        print("\t{0:s}".format(IOIgrac.lijepiString(sorted(list(ruka), reverse = True))))

        # Ucitaj kartu za odigrati ako ima smisla (ako u ruci nije samo 1
        # karta).
        karta = Karta()
        print('Karta:')
        if len(ruka) == 1:
            karta = ruka.pop()
            ruka = {karta}
            print("\t{0:s}".format(IOIgrac.lijepiString(karta)))
        else:
            while True:
                x = six.moves.input("\t")
                try:
                    karta = Karta(x)
                except (TypeError, ValueError):
                    print("Izraz `{0:s}' ne zadaje kartu na valjani nacin.  Pokusaj ponovo!".format(x))
                else:
                    break
            # Ako karti nije zadana boja, pronadi kartu odgovarajuceg znaka u ruci.
            if karta.boja is Karta.Boja.NA:
                if (karta.znak is Karta.Znak.BR2 and any(x == Karta(Karta.Boja.TREF, Karta.Znak.BR2) for x in ruka) or
                    karta.znak is Karta.Znak.BR10 and any(x == Karta(Karta.Boja.KARO, Karta.Znak.BR10) for x in ruka)):
                    # Ako je zadan znak 2/10 i u ruci postoji tref 2/karo 10 i neka druga karta znaka 2/10, provjeri zeli li igrac igrati tref 2/karo 10 ili neku drugu.
                    odgovor = ''
                    if sum(int(x.znak == karta.znak) for x in ruka) > 1:
                        while True:
                            odgovor = six.moves.input("\t\t{0:s}? [D/n] ".format(Karta.Boja.TREF.name.lower() if karta.znak is Karta.Znak.BR2 else Karta.Boja.KARO.name.lower()))
                            if not odgovor or odgovor.upper() in {'D', 'N'}:
                                break
                    if not odgovor or odgovor.upper() == 'D':
                        # Ako igrac zeli igrati tu specijalnu kartu, odaberi ju.
                        karta = (Karta(Karta.Boja.TREF, Karta.Znak.BR2) if karta.znak is Karta.Znak.BR2 else Karta(Karta.Boja.KARO, Karta.Znak.BR10))
                    else:
                        # Inace pronadi (neku) kartu odgovarajuceg znaka u ruci.
                        karta = PohlepniIgrac.slucajniEkvivalentni(ruka, karta)
                else:
                    # Inace pronadi (neku) kartu odgovarajuceg znaka u ruci.
                    karta = PohlepniIgrac.slucajniEkvivalentni(ruka, karta)

        # Pronadi sve moguce poteze s odabranom kartom.
        M = Tablic.moguciPotezi(stol)
        potezi = unijeDisjunktnih(M[karta.znak]) if karta.znak in M else {frozenset()}

        # Ucitaj karte za skupiti ako ima smisla (ako stol nije prazan), a
        # inace vrati zadani potez.
        skupljeno = set()
        print('Za skupiti:')
        if len(potezi) == 1:
            print("\t")
        else:
            citaj = True
            while citaj:
                while True:
                    x = six.moves.input("\t")

                    # Ako je zadan prazni string, prekini ucitavanje.
                    if not x:
                        citaj = False

                        break

                    # Ako je zadano 'AUTO', pronadi najpovoljniji potez.
                    if x.upper() == 'AUTO':
                        potezi = PohlepniIgrac.izborPoteza({karta}, stol)
                        for potez in potezi:
                            if skupljeno <= potez['skupljeno']:
                                for y in sorted(list(potez['skupljeno'] - skupljeno), reverse = True):
                                    print("\t{0:s}".format(IOIgrac.lijepiString(y)))
                                skupljeno = potez['skupljeno']

                                break

                        print("\t")
                        citaj = False

                        break

                    # Inace prevedi unos u kartu.
                    try:
                        x = Karta(x)
                    except (TypeError, ValueError):
                        print("Izraz `{0:s}' ne zadaje kartu na valjani nacin.  Pokusaj ponovo!".format(x))
                    else:
                        break

                if not citaj:
                    break

                if x.boja is Karta.Boja.NA:
                    # Ako karti nije zadana boja, pronadi kartu odgovarajuceg znaka medu preostalim kartama na stolu.  Tref 2 i karo 10 imaju prednost pred ostalim
                    # kartama (ako je medu preostalim kartama npr. 2 karte znaka 10 od kojih je jedna karo 10, implicitno zadavanje '10' prevodi se u karo 10).
                    pronadeno = False
                    if (x.znak in {Karta.Znak.BR2, Karta.Znak.BR10} and
                        any(y in {Karta(Karta.Boja.TREF, Karta.Znak.BR2), Karta(Karta.Boja.KARO, Karta.Znak.BR10)} and y.znak == x.znak for y in stol - skupljeno)):
                        skupljeno |= {Karta(Karta.Boja.TREF, Karta.Znak.BR2) if x.znak is Karta.Znak.BR2 else Karta(Karta.Boja.KARO, Karta.Znak.BR10)}
                        pronadeno = True
                    else:
                        for y in sorted(list(stol - skupljeno), reverse = True):
                            if y.znak == x.znak:
                                skupljeno |= {y}
                                pronadeno = True

                                break
                    if not pronadeno:
                        skupljeno |= {x}
                else:
                    # Inace uzmi eksplicitno zadanu kartu.
                    skupljeno |= {x}

                if not any(skupljeno < potez for potez in potezi):
                    print("\t")
                    citaj = False

        print('')

        # Vrati zadani potez.
        return (karta, skupljeno)
