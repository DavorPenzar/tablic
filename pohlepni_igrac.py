# -*- coding: utf-8 -*-

"""
Implementacija klase igraca igre tablic koji igra pohlepnim algoritmom.

"""

import copy
import random

from skupovi import partitivniSkup, unijeDisjunktnih
from karta import Karta
from engine import Tablic
from pohlepni_log import PohlepniLog

class PohlepniIgrac (Tablic.Igrac):
    """
    Klasa za igraca igre tablic koji igra pohlepnim algoritmom.

    """

    @classmethod
    def izborPoteza (cls, ruka, stol):
        """
        Izracunaj sve moguce poteze i sortiraj ih po korisnosti.

        Funkcija vraca objekt klase list ciji je svaki element objekt klase
        dict i predstavlja tocno jedan moguci (legalni) potez igraca koji u
        ruci sadrzi karte u skupu ruka dok su na stolu karte iz skupa stol.
        Rjecnik svakog poteza sadrzi kljuceve i vrijednosti
            --  'karta' : (Karta), karta iz ruke koju igrac u tom potezu igra,
            --  'skupljeno' : (set), skup karata (Karta) sa stola koje igrac
                skuplja (set() ako se karta samo odlaze na stol),
            --  'tabla' : (bool), skuplja li igrac tim potezom tablu,
            --  'vrijednost' : (int) ako se sa stola tim potezom skupljaju
                karte, ukupna bodovna vrijednost svih skupljenih karata
                (ukljucujuci odigranu), inace bodovna vrijednost suprotna
                vrijednosti odigrane karte,
            --  Karta(Karta.Boja.KARO, Karta.Znak.BR10) : (int), 1 ako se tim
                potezom skuplja karta karo 10, -1 ako se karta karo 10 samo
                odlaze na stol i ne skuplja nista, 0 inace,
            --  Karta(Karta.Boja.TREF, Karta.Znak.BR2) : (int), 1 ako se tim
                potezom skuplja karta tref 2, -1 ako se karta tref 2 samo
                odlaze na stol i ne skuplja nista, 0 inace,
            --  Karta.Znak.A : (int), ukupni broj svih skupljenih karata A
                (ukljucujuci odigranu) ako se tim potezom skupljaju neke karte
                sa stola, -1 ako se karta A samo odlaze na stol i ne skuplja
                nista, 0 inace.
        U povratnoj listi potezi su sortirani silazno leksikografskim uredajem
        koji usporeduje poteze kao uredene 7-orke s vrijednostima
            --  potez['tabla'],
            --  potez['vrijednost'],
            --  len(potez['skupljeno']),
            --  potez[Karta(Karta.Boja.KARO, Karta.Znak.BR10)],
            --  potez[Karta(Karta.Boja.TREF, Karta.Znak.BR2)],
            --  potez[Karta.Znak.A],
            --  14 - int(potez['karta']).

        """

        def __uredaj (x):
            """
            Reprezentiraj potez x kao usporedivi tuple za kljuc sortiranja.

            """

            return (x['tabla'],
                    x['vrijednost'],
                    len(x['skupljeno']),
                    x[Karta(Karta.Boja.KARO, Karta.Znak.BR10)],
                    x[Karta(Karta.Boja.TREF, Karta.Znak.BR2)],
                    x[Karta.Znak.A],
                    14 - int(x['karta']),
                    karta,
                    tuple(sorted(list(x['skupljeno']), reverse = True)))

        # Dohvacanje svih mogucih suma karata sa stola.
        M = Tablic.moguciPotezi(stol)

        # Evaluiranje svih poteza.
        potezi = list()
        for karta in ruka:
            # Racunanje i evaluiranje svih mogucih poteza s igranjem karte
            # karta.
            zaSkupiti = unijeDisjunktnih(M[karta.znak]) if karta.znak in M else {frozenset()}
            for skupljeno in zaSkupiti:
                skupljeno = set(skupljeno)
                potez = {'karta' : karta, 'skupljeno' : copy.deepcopy(skupljeno)}
                if skupljeno:
                    potez.update({'tabla' : skupljeno == stol})
                    skupljeno |= {karta}
                    potez.update({'vrijednost' : Tablic.vrijednostKarata(skupljeno),
                                  Karta(Karta.Boja.KARO, Karta.Znak.BR10) : int(any(x.boja is Karta.Boja.KARO and x.znak is Karta.Znak.BR10 for x in skupljeno)),
                                  Karta(Karta.Boja.TREF, Karta.Znak.BR2) : int(any(x.boja is Karta.Boja.TREF and x.znak is Karta.Znak.BR2 for x in skupljeno)),
                                  Karta.Znak.A : sum(int(x.znak is Karta.Znak.A) for x in skupljeno)})
                else:
                    potez.update({'tabla' : False,
                                  'vrijednost' : -Tablic.vrijednostKarata(karta),
                                  Karta(Karta.Boja.KARO, Karta.Znak.BR10) : -1 if (karta.boja is Karta.Boja.KARO and karta.znak is Karta.Znak.BR10) else 0,
                                  Karta(Karta.Boja.TREF, Karta.Znak.BR2) : -1 if (karta.boja is Karta.Boja.TREF and karta.znak is Karta.Znak.BR2) else 0,
                                  Karta.Znak.A : -1 if karta.znak is Karta.Znak.A else 0})
                potezi.append(potez)

        # Vracanje poteza sortiranih po korisnosti.
        return sorted(potezi, key = __uredaj, reverse = True)

    def __init__ (self, i, ime = None):
        """
        Inicijaliziraj objekt klase PohlepniIgrac.

        """

        Tablic.Igrac.__init__(self, i, ime)

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
        Pohlepnim algoritmom pronadi najpovoljniji potez i odigraj ga.

        Pohlepni algoritam ocituje se u tome sto igrac zapravo trazi (i potom
        ga igra) najpovoljniji prvi potez s danom rukom i danim stolom, bez
        kalkulacija o vec odigranim kartama ili o eventualnom namjernom
        zadrzavanju karata na stolu umjesto moguceg skupljanja, bez
        proracunavanja poteza suigraca i slicnog.

        """

        # Dohvati poteze sortirane po korisnosti.
        potezi = PohlepniIgrac.izborPoteza(ruka, stol)

        if not potezi:
            raise RuntimeError('Pohlepni algoritam nije pronasao nijedan moguci potez.')

        # Slucajnim odabirom odaberi kartu u ruci ekvivalentnu odabranoj
        # pohlepnim algoritmom.
        i = PohlepniLog.prevediKartu(potezi[0]['karta'])
        kandidati = list()
        for x in ruka:
            if PohlepniLog.prevediKartu(x) == i:
                kandidati.append(x)
        potezi[0]['karta'] = random.choice(kandidati)

        # Odigraj trenutno najpovoljniji potez.
        return (potezi[0]['karta'], potezi[0]['skupljeno'])
