"""
Implementacija klase igraca igre tablic koji igra minimax algoritmom.

"""

import copy
import random
import time

from karta import Karta
from engine import Tablic
from pohlepni_log import PohlepniLog
from pohlepni_igrac import PohlepniIgrac

class MinimaxIgrac (Tablic.Igrac):
    """
    Klasa za igraca igre tablic koji igra minimax algoritmom.

    """

    @classmethod
    def vjerojatnaRuka (cls, sigurnoNema, vjerojatnoNema):
        """
        Dohvati vjerojatnu ruku igraca.

        Vjerojatnom rukom igraca smatra se skup onih karata za koje ne vrijedi
        da ih igrac sigurno ili vjerojatno nema.

        Objekt sigurnoNema mora biti objekt klase set ciji su elementi objekti
        klase Karta, a predstavljaju tocno one karte koje igrac sigurno nema
        (zadavajuci i boju i znak).  Objekt vjerojatno nema mora biti lista
        numerickih vrijednosti koja na indeksu i sadrzi ne-nul vrijednost ako i
        samo ako igrac vjerojatno nema kartu/-e koja/-e se pozivom funkcije
        PohlepniLog.prevediKartu prevodi/-e u indeks i.

        Povratna vrijednost funkcije objekt je klase set ciji su elementi
        objekti klase Karta.  Svaka karta koja nije tref 2 ili karo 10, a nije
        takva da ju igrac sigurno ili vjerojatno nema, ima jedinstvenog
        predstavnika elementa u povratnom skupu istog znaka kao ta karta i
        nedefinirane boje (Karta.Boja.NA).  Tref 2 i karo 10 kao eventualne
        predstavnike u povratnom skupu imaju same sebe.

        """

        # Inicijalizacija ruke na prazni skup.
        ruka = set()

        # Trazenje jedinstvenih predstavnika vjerojatnih karata.
        for x in Karta.noviSpil() - sigurnoNema:
            i = PohlepniLog.prevediKartu(x)
            if not vjerojatnoNema[i]:
                ruka |= {Karta(PohlepniLog.prevediIndeks(i))}

        # Vracanje skupa vjerojatnih karata.
        return ruka

    @classmethod
    def heuristika (cls,
                    bodovi, skupljeno,
                    n, i,
                    kraj = False,
                    zadnji = None, stol = set()):
        """
        Izracunaj heursticku vrijednost stanja igre za minimax algoritam.

        Sto je trenutno stanje igre bolje za igraca s indeksom i u igri s n
        igraca, to je heuristicka vrijednost trenutnog stanja veca.

        Objekti bodovi, skupljeno predstavljaju liste numerickih vrijednosti
        duljine n koje na indeksu j sadrze broj skupljenih bodova (ali bez
        vrijednosti karata na stolu za igraca koji je zadnji kupio i bez
        dodanih bodova za strogi maksimum skupljenih karata na kraju igre)
        odnosno broj skupljenih karata (ali bez racunanja karata na stolu koje
        se dodaju igracu koji je zadnji kupio na kraju igre) j-tog igraca u tom
        stanju igre.  Ako je trenutno stanje igre zavrsno (ako je kraj
        vrijednsoti False), prije racunanja heuristicke vrijednosti stanja igre
        igracu s indeksom zadnji (ako zadnji nije None) dodaju se bodovne
        vrijednosti karata na stolu i broj karata na stolu, trazi se igrac sa
        strogo najvise karata i, ako takav postoji, dodaju mu se odgovarajuci
        bodovi.

        Povratna vrijednost je tuple (heurBodovi, heurSkupljeno) gdje je
            1.  heurBodovi  --  suma razlika bodova igraca s indeksom i i
                                ostalih igraca,
            2.  heurSkupljeno   --  suma razlika broja skupljenih karata igraca
                                    s indeksom i i ostalih igraca.

        """

        # Azuriranje varijabli u slucaju kraja igre.
        if kraj:
            if not zadnji is None:
                bodovi[zadnji] += Tablic.vrijednostKarata(stol)
                skupljeno[zadnji] += len(stol)

            M = [0]
            for j in range(1, n):
                if skupljeno[j] > M[0]:
                    M = [j]
                elif skupljeno[j] == M[0]:
                    M.append(j)

            if len(M) == 1:
                bodovi[M[0]] += Tablic.vrijednostMax()

        # Racunanje heuristicke vrijednosti stanja igre.
        heurBodovi = 0
        heurSkupljeno = 0
        for j in range(n):
            heurBodovi += bodovi[i] - bodovi[j]
            heurSkupljeno += skupljeno[i] - skupljeno[j]

        # Vracanje izracunate heuristicke vrijednosti stanja igre.
        return (heurBodovi, heurSkupljeno)

    @classmethod
    def minimax (cls,
                 sigurnoNema, vjerojatnoNema,
                 ruka, stol,
                 bodovi, skupljeno,
                 n, i, j,
                 zadnje = False, zadnji = None,
                 dubina = Tablic.inicijalniBrojKarata_ruka(),
                 T = float('inf')):
        """
        Minimax algoritmom izracunaj najvjerojatniji slijed poteza.

        Od n igraca u igri, referentni (max-igrac i igrac cije su karte zadane
        skupom ruka) je i-ti igrac, a j-ti igrac je trenutno na potezu.
        Trenutno stanje stola zadano je skupom stol.  Trenutno stanje bodova i
        broja skupljenih karata zadano je redom listama bodovi, skupljeno kao u
        funkciji MinimaxIgrac.heuristika.  Igrac koji je trenutno zadnji kupio
        karte zadan je vrijednosti zadnji (kao u funkciji
        MinimaxIgrac.heuristika).  Ako su karte u ruci s kojima se trenutno
        igra podijeljene u zadnjem dijeljenju u igri, zadnje mora biti
        vrijednosti True (radi tocnog racunanja heuristicke vrijednosti listova
        stabla stanja igre).  Objekti sigurnoNema i vjerojatnoNema slicni su
        kao u funkciji MinimaxIgrac.vjerojatnaRuka, samo sto je u ovom slucaju
        vjerojatnoNema ugnjezdena lista duljine n koja na indeksu k zadaje
        listu karata koje k-ti igrac vjerojatno nema (kao u funkciji
        MinimaxIgrac.vjerojatnaRuka).

        Gornja granica dubine stabla stanja igre zadana je vrijednosti dubina,
        ali tako da se jednom razinom dubine smatra niz poteza svih igraca
        (odnosno prvom razinom niz poteza od j-tog igraca do (n - 1)-tog igraca
        ukljucivo).  Konkretno, gornja granica dubine stabla stanja igre iznosi
        n * dubina - j.  Ako se algoritam izvrsava dulje od T sekundi,
        izvrsavanje se prekida i vraca se dosad najvjerojatniji pronadeni
        slijed poteza u igri.

        Povratna vrijednost lista je objekata klase dict koji zadaju redom
        poteze igraca s indeksima j, j + 1, j + 2, ..., n - 1, 0, 1, ...
        Rjecnik svakog poteza sadrzi kljuceve i vrijednosti
            --  'karta' : (Karta), karta iz ruke koju igrac u tom potezu igra,
            --  'skupljeno' : (set), skup karata (Karta) sa stola koje igrac
                skuplja (set() ako se karta samo odlaze na stol).

        """

        # Inicijalizacija pocetnog trenutka mjerenja vremena na trenutno
        # vrijeme.
        t0 = time.time()

        def __minimax (sigurnoNema, vjerojatnoNema,
                       ruka, stol,
                       bodovi, skupljeno,
                       n, i, j,
                       zadnje, zadnji,
                       dubina,
                       alpha, beta):
            """
            Minimax algoritam s alpha/beta-podrezivanjem.

            Istoimeni argumenti jednakog su znacenja kao u funkciji
            MinimaxIgrac.minimax, a argumenti alpha, beta dvoclani su tuple-ovi
            (dosad pronadene heuristicke najvise max- i najnize
            min-vrijednosti).

            """

            # Prekidanje pretrazivanja stabla u dubinu u slucaju nekog od
            # terminalnih uvjeta (stanje bez potomaka, maksimalna duljina ili
            # vremensko prekoracenje).
            if not (j or ruka) or not dubina or time.time() - t0 > T:
                return (list(), MinimaxIgrac.heuristika(bodovi, skupljeno,
                                                        n, i,
                                                        zadnje and j == 0 and not ruka,
                                                        zadnji, stol))

            # Granaje u ovisnosti o igracu na potezu.

            # Inicijalizacija najvjerojatnijeg slijeda poteza (grana),
            # njegove heuristicke vrijednosti (vrijednost) i zadnjeg
            # promatranog poteza (zadnjiPotez).
            grana = list()
            vrijednost = (-float('inf'), -float('inf'))
            zadnjiPotez = (Karta(), list())

            # Iteriranje po mogucim potezima.
            for potez in PohlepniIgrac.izborPoteza(ruka if j == i else MinimaxIgrac.vjerojatnaRuka(sigurnoNema, vjerojatnoNema[j]), stol):
                # Racunanje "protoripa poteza" (izgled poteza neovisno o bojama karata osim u slucaju specijalnih karata --- tref 2 i karo 10) i
                # provjera je li takav potez vec obraden (ako je, obrada se preskce).
                ovajPotez = (Karta(PohlepniLog.prevediIndeks(PohlepniLog.prevediKartu(potez['karta']))),
                             sorted([Karta(PohlepniLog.prevediIndeks(PohlepniLog.prevediKartu(x))) for x in potez['skupljeno']], reverse = True))
                if ovajPotez == zadnjiPotez:
                    continue
                else:
                    # Ako ovakav potez jos nije obraden, spremanje njegovog
                    # prototipa u varijablu zadnjiPotez.
                    zadnjiPotez = ovajPotez

                # Zadavanje boje odigranoj karti (zbog njezine znacajnosti nakon dodavanja u skup sigurnoNema) ako nije
                # definirana.
                if potez['karta'].znak is Karta.Znak.NA:
                    for boja in sorted([Karta.Boja.HERC, Karta.Boja.PIK, Karta.Boja.KARO, Karta.Boja.TREF], reverse = True):
                        if potez['karta'].znak is Karta.Znak.BR2 and boja is Karta.Boja.TREF:
                            continue
                        elif potez['karta'].znak is Karta.Znak.BR10 and boja is Karta.Boja.KARO:
                            continue
                        if not Karta(boja, potez['karta'].znak) in sigurnoNema:
                            potez['karta'].boja = boja

                            break

                # Kreiranje novih lista bodova i brojeva skupljenih karata.
                noviBodovi = copy.deepcopy(bodovi)
                novoSkupljeno = copy.deepcopy(skupljeno)
                noviBodovi[j] += (potez['vrijednost'] + int(potez['tabla']) * Tablic.vrijednostTable())
                if potez['skupljeno']:
                    novoSkupljeno[j] += 1 + len(potez['skupljeno'])

                # Rekurzivno trazenje najvjerojatnijeg potomka trenutnog
                # poteza.
                sadGrana, sadVrijednost = __minimax(sigurnoNema | {potez['karta']}, vjerojatnoNema,
                                                    ruka - {potez['karta']} if j == i else ruka, stol - potez['skupljeno'] if potez['skupljeno'] else stol | {potez['karta']},
                                                    noviBodovi, novoSkupljeno,
                                                    n, i, (j + 1) % n,
                                                    zadnje, j if potez['skupljeno'] else zadnji,
                                                    dubina if (j + 1) % n else (dubina - 1),
                                                    alpha, beta)

                # Usporedba pronadenog najvjerojatnijeg slijeda nakon ovog
                # poteza s dosad pronadenim najvjerojatnijim slijedom i
                # adekvatno azuriranje varijabli.
                if j == i:
                    # Max-igrac je na redu.
                    if len(sadGrana) + 1 > len(grana) or len(sadGrana) + 1 == len(grana) and sadVrijednost > vrijednost:
                        grana = [{'karta' : potez['karta'], 'skupljeno' : potez['skupljeno']}] + sadGrana
                        vrijednost = sadVrijednost
                    elif len(sadGrana) + 1 < len(grana):
                        # Ako je algoritam morao zavrsiti prije dosega
                        # maksimalne dubine ili stanja bez potomka, to znaci
                        # dvije stvari:
                        # 1.  slijed najvjerojatnijih poteza bit ce kraci,
                        # 2.  terminalni uvjet bio je vremensko prekoracenje.
                        # U tom slucaju pretrazivanje poteza moze se prekinuti
                        # (svaka sljedeca provjera takoder ce doseci terminalni
                        # uvjet vremenskog prekoracenja).
                        break
                    if vrijednost > alpha:
                        alpha = vrijednost
                else:
                    # Jedan od min-igraca je na redu.
                    if len(sadGrana) + 1 > len(grana) or len(sadGrana) + 1 == len(grana) and sadVrijednost < vrijednost:
                        grana = [{'karta' : potez['karta'], 'skupljeno' : potez['skupljeno']}] + sadGrana
                        vrijednost = sadVrijednost
                    elif len(sadGrana) + 1 < len(grana):
                        # Ako je algoritam morao zavrsiti prije dosega
                        # maksimalne dubine ili stanja bez potomka, to znaci
                        # dvije stvari:
                        # 1.  slijed najvjerojatnijih poteza bit ce kraci,
                        # 2.  terminalni uvjet bio je vremensko prekoracenje.
                        # U tom slucaju pretrazivanje poteza moze se prekinuti
                        # (svaka sljedeca provjera takoder ce doseci terminalni
                        # uvjet vremenskog prekoracenja).
                        break
                    if vrijednost < beta:
                        beta = vrijednost

                if alpha >= beta:
                    break

            # Vracanje najvjerojatnijeg slijeda poteza i njegove
            # heuristicke vrijednosti.
            return (grana, vrijednost)

        # Racunanje najvjerojatnijeg slijeda poteza i njegove heuristicke
        # vrijednosti minimax algoritmom.
        grana, vrijednost = __minimax(sigurnoNema, vjerojatnoNema,
                                      ruka, stol,
                                      bodovi, skupljeno,
                                      n, i, j,
                                      zadnje, zadnji,
                                      dubina,
                                      (-float('inf'), -float('inf')),
                                      (float('inf'), float('inf')))

        # Vracanje izracunatog najvjerojatnijeg slijeda poteza.
        return grana

    def __init__ (self, i, ime = None, maxDubina = Tablic.inicijalniBrojKarata_ruka(), maxT = float('inf')):
        """
        Inicijaliziraj objekt klase MinimaxIgrac.

        Argumenti maxDubina, maxT zadaju parametre dubina, T u funkciji
        MinimaxIgrac pri racunanju sljedeceg poteza.  Nakon zadnjeg dijeljenja
        za dubinu se uzima vrijednost Tablic.inicijalniBrojKarata_ruka(),
        neovisno o argumentu maxDubina.

        """

        Tablic.Igrac.__init__(self, i, ime)

        self.__maxDubina = maxDubina
        self.__maxT = maxT

        # Inicijalizacija relevantnih varijabli.

        self.__k = None # broj karata u spilu

        self.__n = None # broj igraca

        self.__bodovi = None
        self.__skupljeno = None

        self.__zadnji = None

        self.__sigurnoNema = None
        self.__vjerojatnoNema = None

    def __copy__ (self):
        igrac = MinimaxIgrac(self.dohvatiIndeks(), self.dohvatiIme(), self.__maxDubina, self.__maxT)

        igrac.__k = self.__k

        igrac.__n = self.__n

        igrac.__bodovi = self.__bodovi
        igrac.__skupljeno = self.__skupljeno

        igrac.__zadnji = self.__zadnji

        igrac.__sigurnoNema = self.__sigurnoNema
        igrac.__vjerojatnoNema = self.__vjerojatnoNema

        return igrac

    def __deepcopy__ (self, memodict = dict()):
        igrac = MinimaxIgrac(copy.deepcopy(self.dohvatiIndeks(), memodict), copy.deepcopy(self.dohvatiIme(), memodict), copy.deepcopy(self.__maxDubina, memodict), copy.deepcopy(self.__maxT, memodict))

        igrac.__k = copy.deepcopy(self.__k, memodict)

        igrac.__n = copy.deepcopy(self.__n, memodict)

        igrac.__bodovi = copy.deepcopy(self.__bodovi, memodict)
        igrac.__skupljeno = copy.deepcopy(self.__skupljeno, memodict)

        igrac.__zadnji = copy.deepcopy(self.__zadnji, memodict)

        igrac.__sigurnoNema = copy.deepcopy(self.__sigurnoNema, memodict)
        igrac.__vjerojatnoNema = copy.deepcopy(self.__vjerojatnoNema, memodict)

        return igrac

    def hocuRazlog (self):
        return False

    def saznajBrojIgraca (self, n, imena):
        """
        Pripremi se za igranje nove igre od n igraca.

        """

        # Postavljanje pocetnih vrijednosti relevantnih varijabli.

        self.__k = 52 - Tablic.inicijalniBrojKarata_stol()
        self.__n = n

        self.__bodovi = [0 for i in range(self.__n)]
        self.__skupljeno = [0 for i in range(self.__n)]

        self.__zadnji = None

        self.__sigurnoNema = set()
        self.__vjerojatnoNema = [[None if j == self.dohvatiIndeks() else 0 for i in range(PohlepniLog.dohvatiBrojIndeksa())] for j in range(self.__n)]

    def saznajNovoDijeljenje (self, ruka, stol):
        """
        Pripremi se zaa novu etapu igre.

        """

        # Azuriranje broja preostalih karata u spilu.
        self.__k -= self.__n * len(ruka)

        # Azuriranje podataka o kartama koje igraci sigurno nemaju i
        # resetiranje podataka o kartama koje igraci vjerojatno nemaju.
        self.__sigurnoNema |= ruka | stol
        self.__vjerojatnoNema = [[None if j == self.dohvatiIndeks() else 0 for i in range(PohlepniLog.dohvatiBrojIndeksa())] for j in range(self.__n)]

    def vidiPotez (self, i, ruka, stol, karta, skupljeno):
        """
        Azuriraj znanja i pretpostavke o trenutnoj igri.

        """

        # Azuriranje varijabli ako je igrac kupio karte.
        if skupljeno:
            self.__bodovi[i] += Tablic.vrijednostKarata({karta} | skupljeno) + int(skupljeno == stol) * Tablic.vrijednostTable()
            self.__skupljeno[i] += 1 + len(skupljeno)

            self.__zadnji = i

        # Azuriranje podataka o kartama koje i-ti igrac vjerojatno nema ako
        # zadnje dijeljenje nije bilo posljednje u igri i ako i-ti igrac nije
        # ovaj igrac.
        if self.__k and i != self.dohvatiIndeks():
            karta_indeks = PohlepniLog.prevediKartu(karta)

            # Nakon sto je odigrao ovu kartu, nije poznato ima li i-ti igrac
            # jos takvih karata pa se ne pretpostavlja da ih nema.
            self.__vjerojatnoNema[i][karta_indeks] = 0

            # Ako igrac nije nista kupio sa stola, pregledavanje podigranih karata (znakova).  Podigranim
            # kartama smatraju se karte znakova koji se prije dodavanja ove karte nisu mogli zbrojiti na stolu i,
            # ako se znak ove karte vec nalazi na stolu, karte tog znaka.
            if skupljeno:
                podigrani = set()
            else:
                podigrani = set(Tablic.moguciPotezi(stol | {karta}).keys()) - set(Tablic.moguciPotezi(stol).keys())
                if any(x.znak == karta.znak for x in stol):
                    podigrani |= {karta.znak}

            # Za svaku od podigranih karata odustajanje od pretpostavki da i-ti igrac nema takvu kartu.
            for x in podigrani:
                if (x is Karta.Znak.BR2 and not self.__vjerojatnoNema[i][PohlepniLog.prevediKartu(Karta(Karta.Boja.TREF, Karta.Znak.BR2))] is None):
                    self.__vjerojatnoNema[i][PohlepniLog.prevediKartu(Karta(Karta.Boja.TREF, Karta.Znak.BR2))] = 0
                elif (x is Karta.Znak.BR10 and not self.__vjerojatnoNema[i][PohlepniLog.prevediKartu(Karta(Karta.Boja.KARO, Karta.Znak.BR10))] is None):
                    self.__vjerojatnoNema[i][PohlepniLog.prevediKartu(Karta(Karta.Boja.KARO, Karta.Znak.BR10))] = 0
                if not self.__vjerojatnoNema[i][PohlepniLog.prevediKartu(Karta(x))]:
                    self.__vjerojatnoNema[i][PohlepniLog.prevediKartu(Karta(x))] = 0

            # Racunanje vrijednosti odigranog poteza i karata koje i-ti igrac vjerojatno ima.
            vrijednost = ((Tablic.vrijednostKarata(skupljeno | {karta}) + int(skupljeno == stol) * Tablic.vrijednostTable()) if skupljeno else 0)
            tudaRuka = MinimaxIgrac.vjerojatnaRuka(self.__sigurnoNema, self.__vjerojatnoNema[i])

            # Za svaki potez vrijedniji od odigranog, a koji ne zahtijeva igranje odigrane karte, uvecanje vrijednosti da igrac
            # nema kartu kojom se taj potez igra.
            for potez in PohlepniIgrac.izborPoteza(tudaRuka, stol):
                if (potez['vrijednost'] + int(potez['tabla']) * Tablic.vrijednostTable() < vrijednost or
                    potez['vrijednost'] + int(potez['tabla']) * Tablic.vrijednostTable() == vrijednost and len(potez['skupljeno']) <= len(skupljeno)):
                    break
                if PohlepniLog.prevediKartu(potez['karta']) == karta_indeks or potez['karta'].znak in podigrani:
                    continue
                self.__vjerojatnoNema[i][PohlepniLog.prevediKartu(potez['karta'])] = 1

        # Azuriranje podataka o kartama koje igraci sigurno nemaju.
        self.__sigurnoNema |= {karta}

        if self.__k and sum(int(x.znak == karta.znak) for x in self.__sigurnoNema) == 4:
            R = [PohlepniLog.prevediKartu(Karta(karta.znak))]
            if karta.znak is Karta.Znak.BR2:
                R.append(PohlepniLog.prevediKartu(Karta(Karta.Boja.TREF, Karta.Znak.BR2)))
            elif karta.znak is Karta.Znak.BR10:
                R.append(PohlepniLog.prevediKartu(Karta(Karta.Boja.KARO, Karta.Znak.BR10)))

            for j in range(self.__n):
                if j != self.dohvatiIndeks():
                    for r in R:
                        self.__vjerojatnoNema[j][r] = None

    def odigraj (self, ruka, stol, ponovi = False):
        """
        Minimax algoritmom pronadi najpovoljniji potez i odigraj ga.

        """

        # Dohvati najvjerojatniji slijed poteza.
        grana = MinimaxIgrac.minimax(self.__sigurnoNema, self.__vjerojatnoNema,
                                     ruka, stol,
                                     self.__bodovi, self.__skupljeno,
                                     self.__n, self.dohvatiIndeks(), self.dohvatiIndeks(),
                                     not self.__k, self.__zadnji,
                                     self.__maxDubina if self.__k else Tablic.inicijalniBrojKarata_ruka(),
                                     self.__maxT)

        if not grana:
            raise RuntimeError('Minimax algoritam nije pronasao nijedan moguci potez.')

        # Slucajnim odabirom odaberi kartu u ruci ekvivalentnu odabranoj
        # minimax algoritmom.
        i = PohlepniLog.prevediKartu(grana[0]['karta'])
        kandidati = list()
        for x in ruka:
            if PohlepniLog.prevediKartu(x) == i:
                kandidati.append(x)
        grana[0]['karta'] = random.choice(kandidati)

        # Odigraj najpovoljniji potez.
        return (grana[0]['karta'], grana[0]['skupljeno'])

    def dohvatiMaxDubinu (self):
        """
        Dohvati koristenu dubinu minimax algoritma.

        """

        return self.__maxDubina

    def dohvatiMaxT (self):
        """
        Dohvati vremensko ogranicenje minimax algoritma.

        """

        return self.__maxT

    def dohvatiBodove (self, i = None):
        """
        Dohvati trenutno bodovno stanje.

        Ako i nije None, povratna vrijednost su bodovi i-tog igraca.  Ako je i
        None, onda je povratna vrijednost lista kojoj su na k-tom mjestu bodovi
        k-tog igraca.

        """

        if not i is None:
            return self.__bodovi[i]

        return copy.deepcopy(self.__bodovi)

    def dohvatiSkupljeno (self, i = None):
        """
        Dohvati trenutno stanje broja skupljenih karata.

        Ako i nije None, povratna vrijednost je broj skupljenih karata i-tog
        igraca.  Ako je i None, onda je povratna vrijednost lista kojoj je na
        k-tom mjestu broj skupljenih karata k-tog igraca.

        """

        if not i is None:
            return self.__skupljeno[i]

        return copy.deepcopy(self.__skupljeno)

    def dohvatiZadnjeg (self):
        """
        Dohvati informaciju o tome tko je zadnji kupio.

        """

        return self.__zadnji

    def dohvatiSigurnoNema (self):
        """
        Dohvati trenutna saznanja o kartama koje igraci sigurno nemaju.

        """

        return copy.deepcopy(self.__sigurnoNema)

    def dohvatiVjerojatnoNema (self, i = None):
        """
        Dohvati trenutna saznanja o kartama koje igraci vjerojatno nemaju.

        Ako i nije None, povratna vrijednost sukladna je argumentu
        vjerojatnoNema u funkciji MinimaxIgrac.vjerojatna ruka.  Ako je i None,
        onda je povratna vrijednost ugnjezdena lista kojoj je na k-tom mjestu
        lista koja bi se dobila pozivom self.vjerojatnoNema(k).

        """

        if i is None:
            return copy.deepcopy(self.__vjerojatnoNema)

        return copy.deepcopy(self.__vjerojatnoNema[i])
