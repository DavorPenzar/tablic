"""
Implementacija klasa igraca igre tablic koji igraju minimax algoritmom.

"""

import copy
import math
import random
import time

from karta import Karta
from engine import Tablic
from pohlepni_log import PohlepniLog1
from pohlepni_igrac import PohlepniIgrac1

class MinimaxIgrac1 (Tablic.Igrac):
    """
    Klasa za igraca igre tablic koji igra obicnim minimax algoritmom.

    """

    @classmethod
    def vjerojatnaRuka (cls, sigurnoNema : set, vjerojatnoNema : list) -> set:
        """
        Dohvati vjerojatnu ruku igraca.

        Vjerojatnom rukom igraca smatra se skup onih karata za koje ne vrijedi da ih
        igrac sigurno ili vjerojatno nema.

        Objekt sigurnoNema mora biti objekt klase set ciji su elementi objekti klase
        Karta, a predstavljaju tocno one karte koje igrac sigurno nema (zadavajuci i
        boju i znak).  Objekt vjerojatno nema mora biti lista numerickih vrijednosti
        koja na indeksu i sadrzi strogo pozitivnu vrijednost ako i samo ako igrac
        vjerojatno nema kartu/-e koja/-e se pozivom funkcije PohlepniLog1.prevediKartu
        prevodi/-e u indeks i.

        Povratna vrijednost funkcije objekt je klase set ciji su elementi objekti klase
        Karta.  Svaka karta koja nije tref 2 ili karo 10, a nije takva da ju igrac
        sigurno ili vjerojatno nema, ima jedinstvenog predstavnika elementa u povratnom
        skupu istog znaka kao ta karta i nedefinirane boje (Karta.Boja.NA).  Tref 2 i
        karo 10 kao eventualne predstavnike u povratnom skupu imaju same sebe.

        """

        # Inicijalizacija ruke na prazni skup.
        ruka = set()

        # Trazenje jedinstvenih predstavnika vjerojatnih karata.
        for x in Tablic.noviSpil() - sigurnoNema:
            i = PohlepniLog1.prevediKartu(x)
            if vjerojatnoNema[i] <= 0:
                ruka |= {Karta(PohlepniLog1.prevediIndeks(i))}

        # Vracanje skupa vjerojatnih karata.
        return ruka

    @classmethod
    def heuristika (cls,
                    bodovi : list, skupljeno : list,
                    n : int, i : int,
                    kraj : bool = False,
                    zadnji = None, stol : set = set()) -> tuple:
        """
        Izracunaj heursticku vrijednost stanja igre za minimax algoritam.

        Sto je trenutno stanje igre bolje za igraca s indeksom i u igri s n igraca, to
        je heuristicka vrijednost trenutnog stanja veca.

        Objekti bodovi, skupljeno predstavljaju liste numerickih vrijednosti duljine n
        koje na indeksu j sadrze broj skupljenih bodova (ali bez vrijednosti karata na
        stolu za igraca koji je zadnji kupio i bez dodanih bodova za strogi maksimum
        skupljenih karata na kraju igre) odnosno broj skupljenih karata (ali bez
        racunanja karata na stolu koje se dodaju igracu koji je zadnji kupio na kraju
        igre) j-tog igraca u tom stanju igre.  Ako je trenutno stanje igre zavrsno (ako
        je kraj vrijednsoti False), prije racunanja heuristicke vrijednosti stanja igre
        igracu s indeksom zadnji (ako zadnji nije None) dodaju se bodovne vrijednosti
        karata na stolu i broj karata na stolu, trazi se igrac sa strogo najvise karata
        i, ako takav postoji, dodaju mu se odgovarajuci bodovi.

        Povratna vrijednost je tuple (heurBodovi, heurSkupljeno) gdje je
            1.  heurBodovi  --  suma razlika bodova igraca s indeksom i i ostalih
                                igraca,
            2.  heurSkupljeno   --  suma razlika broja skupljenih karata igraca s
                                    indeksom i i ostalih igraca.

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
                 sigurnoNema : set, vjerojatnoNema : list,
                 ruka : set, stol : set,
                 bodovi : list, skupljeno : list,
                 n : int, i : int, j : int,
                 zadnje : bool = False, zadnji = None,
                 dubina : int = Tablic.inicijalniBrojKarata_ruka(), T : float = math.inf) -> list:
        """
        Minimax algoritmom izracunaj najvjerojatniji slijed poteza.

        Od n igraca u igri, referentni (max-igrac i igrac cije su karte zadane skupom
        ruka) je i-ti igrac, a j-ti igrac je trenutno na potezu.  Trenutno stanje stola
        zadano je skupom stol.  Trenutno stanje bodova i broja skupljenih karata zadano
        je redom listama bodovi, skupljeno kao u funkciji MinimaxIgrac1.heuristika.
        Igrac koji je trenutno zadnji kupio karte zadan je vrijednosti zadnji (kao u
        funkciji MinimaxIgrac1.heuristika).  Ako su karte u ruci s kojima se trenutno
        igra podijeljene u zadnjem dijeljenju u igri, zadnje mora biti vrijednosti True
        (radi tocnog racunanja heuristicke vrijednosti listova stabla stanja igre).

        Objekti sigurnoNema i vjerojatnoNema slicni su kao u funkciji
        MinimaxIgrac1.vjerojatnaRuka, samo sto je u ovom slucaju vjerojatnoNema
        ugnjezdena lista duljine n koja na indeksu k zadaje listu karata koje k-ti
        igrac vjerojatno nema (kao u funkciji MinimaxIgrac1.vjerojatnaRuka).

        Gornja granica dubine stabla stanja igre zadana je vrijednosti dubina, ali tako
        da se jednom razinom dubine smatra niz poteza svih igraca (odnosno prvom
        razinom niz poteza od j-tog igraca do (n - 1)-tog igraca ukljucivo).
        Konkretno, gornja granica dubine stabla stanja igre iznosi n * dubina - j.  Ako
        se algoritam izvrsava dulje od T sekundi, izvrsavanje se prekida i vraca se
        dosad najvjerojatniji pronadeni slijed poteza u igri.

        Povratna vrijednost lista je objekata klase dict koji zadaju redom poteze
        igraca s indeksima j, j + 1, j + 2, ..., n - 1, 0, 1, ...  Rjecnik svakog
        poteza sadrzi kljuceve i vrijednosti
            --  'karta' : (Karta), karta iz ruke koju igrac u tom potezu igra,
            --  'skupljeno' : (set), skup karata (Karta) sa stola koje igrac skuplja
                (set() ako se karta samo odlaze na stol).

        """

        # Inicijalizacija pocetnog trenutka mjerenja vremena na trenutno vrijeme.
        t0 = time.time()

        def __minimax (sigurnoNema : set, vjerojatnoNema : list,
                       ruka : set, stol : set,
                       bodovi : list, skupljeno : list,
                       n : int, i : int, j : int,
                       zadnje : bool, zadnji,
                       dubina : int,
                       alpha : tuple, beta : tuple) -> tuple:
            """
            Minimax algoritam s alpha/beta-podrezivanjem.

            Istoimeni argumenti jednakog su znacenja kao u funkciji MinimaxIgrac1.minimax,
            a argumenti alpha, beta dvoclani su tuple-ovi (dosad pronadene heuristicke
            najvise max- i najnize min-vrijednosti).

            """

            # Prekidanje pretrazivanja stabla u dubinu u slucaju nekog od terminalnih uvjeta (stanje bez potomaka, maksimalna duljina ili vremensko prekoracenje).
            if not (j or ruka) or not dubina or time.time() - t0 > T:
                return ([],
                        MinimaxIgrac1.heuristika(copy.deepcopy(bodovi), copy.deepcopy(skupljeno),
                                                 n, i,
                                                 zadnje and j == 0 and not ruka,
                                                 zadnji, stol))

            # Granaje u ovisnosti o igracu na potezu.

            if j == i:
                # Max-igrac je na potezu.

                # Inicijalizacija najvjerojatnijeg slijeda poteza (grana), njegove heuristicke vrijednosti (vrijednost) i zadnjeg promatranog poteza (zadnjiPotez).
                grana = []
                vrijednost = (-math.inf, -math.inf)
                zadnjiPotez = (Karta(), [])

                # Iteriranje po mogucim potezima.
                for potez in PohlepniIgrac1.izborPoteza(ruka, stol):
                    # Racunanje "protoripa poteza" (izgled poteza neovisno o bojama karata osim u slucaju specijalnih karata --- tref 2 i karo 10) i provjera je li takav potez vec obraden (ako je, obrada se preskce).
                    ovajPotez = (Karta(PohlepniLog1.prevediIndeks(PohlepniLog1.prevediKartu(potez['karta']))),
                                 sorted([Karta(PohlepniLog1.prevediIndeks(PohlepniLog1.prevediKartu(x))) for x in potez['skupljeno']], reverse = True))
                    if ovajPotez == zadnjiPotez:
                        continue
                    else:
                        # Ako ovakav potez jos nije obraden, spremanje njegovog prototipa u varijablu zadnjiPotez.
                        zadnjiPotez = ovajPotez

                    # Kreiranje novih lista bodova i brojeva skupljenih karata.
                    noviBodovi = copy.deepcopy(bodovi)
                    novoSkupljeno = copy.deepcopy(skupljeno)
                    noviBodovi[i] += potez['vrijednost'] + int(potez['tabla']) * Tablic.vrijednostTable()
                    if potez['skupljeno']:
                        novoSkupljeno[i] += 1 + len(potez['skupljeno'])

                    # Rekurzivno trazenje najvjerojatnijeg potomka trenutnog poteza.
                    sadGrana, sadVrijednost = __minimax(copy.deepcopy(sigurnoNema | {potez['karta']}), copy.deepcopy(vjerojatnoNema),
                                                        copy.deepcopy(ruka - {potez['karta']}), copy.deepcopy(stol - potez['skupljeno']) if potez['skupljeno'] else copy.deepcopy(stol | {potez['karta']}),
                                                        noviBodovi, novoSkupljeno,
                                                        n, i, (j + 1) % n,
                                                        zadnje, i if potez['skupljeno'] else zadnji,
                                                        dubina if (j + 1) % n else (dubina - 1),
                                                        copy.deepcopy(alpha), copy.deepcopy(beta))

                    # Usporedba pronadenog najvjerojatnijeg slijeda nakon ovog poteza s dosad pronadenim najvjerojatnijim slijedom i adekvatno azuriranje varijabli.
                    if len(sadGrana) + 1 > len(grana) or len(sadGrana) + 1 == len(grana) and sadVrijednost > vrijednost:
                        grana = [{'karta' : potez['karta'], 'skupljeno' : potez['skupljeno']}] + sadGrana
                        vrijednost = sadVrijednost
                    elif len(sadGrana) + 1 < len(grana):
                        # Ako je algoritam morao zavrsiti prije dosega maksimalne dubine ili stanja bez potomka, to znaci dvije stvari:
                        # 1.  slijed najvjerojatnijih poteza bit ce kraci,
                        # 2.  terminalni uvjet bio je vremensko prekoracenje.
                        # U tom slucaju pretrazivanje poteza moze se prekinuti (svaka sljedeca provjera takoder ce doseci terminalni uvjet vremenskog prekoracenja).
                        break
                    if vrijednost > alpha:
                        alpha = vrijednost
                    if alpha >= beta:
                        break

                # Vracanje najvjerojatnijeg slijeda poteza i njegove heuristicke vrijednosti.
                return (grana, vrijednost)
            else:
                # Na potezu je ntko od min-igraca.

                # Inicijalizacija najvjerojatnijeg slijeda poteza (grana), njegove heuristicke vrijednosti (vrijednost) i zadnjeg promatranog poteza (zadnjiPotez).
                grana = []
                vrijednost = (math.inf, math.inf)
                tudaRuka = MinimaxIgrac1.vjerojatnaRuka(copy.deepcopy(sigurnoNema), copy.deepcopy(vjerojatnoNema[j]))
                zadnjiPotez = (Karta(), [])

                # Iteriranje po mogucim potezima.
                for potez in PohlepniIgrac1.izborPoteza(tudaRuka, stol):
                    # Racunanje "protoripa poteza" (izgled poteza neovisno o bojama karata osim u slucaju specijalnih karata --- tref 2 i karo 10) i provjera je li takav potez vec obraden (ako je, obrada se preskce).
                    ovajPotez = (Karta(PohlepniLog1.prevediIndeks(PohlepniLog1.prevediKartu(potez['karta']))),
                                 sorted([Karta(PohlepniLog1.prevediIndeks(PohlepniLog1.prevediKartu(x))) for x in potez['skupljeno']], reverse = True))
                    if ovajPotez == zadnjiPotez:
                        continue
                    else:
                        # Ako ovakav potez jos nije obraden, spremanje njegovog prototipa u varijablu zadnjiPotez.
                        zadnjiPotez = ovajPotez

                    # Zadavanje boje odigranoj karti (zbog njezine znacajnosti nakon dodavanja u skup sigurnoNema) ako nije definirana.
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
                    noviBodovi[j] += potez['vrijednost'] + int(potez['tabla']) * Tablic.vrijednostTable()
                    if potez['skupljeno']:
                        novoSkupljeno[j] += 1 + len(potez['skupljeno'])

                    # Rekurzivno trazenje najvjerojatnijeg potomka trenutnog poteza.
                    sadGrana, sadVrijednost = __minimax(copy.deepcopy(sigurnoNema | {potez['karta']}), copy.deepcopy(vjerojatnoNema),
                                                        copy.deepcopy(ruka), copy.deepcopy(stol - potez['skupljeno']) if potez['skupljeno'] else copy.deepcopy(stol | {potez['karta']}),
                                                        noviBodovi, novoSkupljeno,
                                                        n, i, (j + 1) % n,
                                                        zadnje, j if potez['skupljeno'] else zadnji,
                                                        dubina if (j + 1) % n else (dubina - 1),
                                                        copy.deepcopy(alpha), copy.deepcopy(beta))

                    # Usporedba pronadenog najvjerojatnijeg slijeda nakon ovog poteza s dosad pronadenim najvjerojatnijim slijedom i adekvatno azuriranje varijabli.
                    if len(sadGrana) + 1 > len(grana) or len(sadGrana) + 1 == len(grana) and sadVrijednost < vrijednost:
                        grana = [{'karta' : potez['karta'], 'skupljeno' : potez['skupljeno']}] + sadGrana
                        vrijednost = sadVrijednost
                    elif len(sadGrana) + 1 < len(grana):
                        # Ako je algoritam morao zavrsiti prije dosega maksimalne dubine ili stanja bez potomka, to znaci dvije stvari:
                        # 1.  slijed najvjerojatnijih poteza bit ce kraci,
                        # 2.  terminalni uvjet bio je vremensko prekoracenje.
                        # U tom slucaju pretrazivanje poteza moze se prekinuti (svaka sljedeca provjera takoder ce doseci terminalni uvjet vremenskog prekoracenja).
                        break
                    if vrijednost < beta:
                        beta = vrijednost
                    if beta <= alpha:
                        break

                # Vracanje najvjerojatnijeg slijeda poteza i njegove heuristicke vrijednosti.
                return (grana, vrijednost)

        # Racunanje najvjerojatnijeg slijeda poteza i njegove heuristicke vrijednosti minimax algoritmom.
        grana, vrijednost = __minimax(copy.deepcopy(sigurnoNema), copy.deepcopy(vjerojatnoNema),
                                      copy.deepcopy(ruka), copy.deepcopy(stol),
                                      copy.deepcopy(bodovi), copy.deepcopy(skupljeno),
                                      n, i, j,
                                      zadnje, zadnji,
                                      dubina,
                                      copy.deepcopy((-math.inf, -math.inf)), copy.deepcopy((math.inf, math.inf)))

        # Vracanje izracunatog najvjerojatnijeg slijeda poteza.
        return grana

    def __init__ (self, i : int, ime = None, maxDubina : int = Tablic.inicijalniBrojKarata_ruka(), maxT : float = math.inf):
        """
        Inicijaliziraj objekt klase MinimaxIgrac1.

        Argumenti maxDubina, maxT zadaju parametre dubina, T u funkciji MinimaxIgrac1
        pri racunanju sljedeceg poteza.

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

    def hocuRazlog (self):
        return False

    def saznajBrojIgraca (self, n : int):
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
        self.__vjerojatnoNema = [[0 for i in range(PohlepniLog1.dohvatiBrojIndeksa())] for j in range(self.__n)]

    def saznajNovoDijeljenje (self, ruka : set, stol : set):
        """
        Pripremi se zaa novu etapu igre.

        """

        # Azuriranje broja preostalih karata u spilu.
        self.__k -= self.__n * len(ruka)

        # Azuriranje podataka o kartama koje igraci sigurno nemaju i resetiranje podataka o kartama koje igraci vjerojatno nemaju.
        self.__sigurnoNema |= (ruka | stol)
        self.__vjerojatnoNema = [[0 for i in range(PohlepniLog1.dohvatiBrojIndeksa())] for j in range(self.__n)]

    def vidiPotez (self, i : int, ime : str, ruka : set, stol : set, karta : Karta, skupljeno : set):
        """
        Azuriraj znanja i pretpostavke o trenutnoj igri s obzirom na odigrani potez.

        """

        # Azuriranje varijabli ako je igrac kupio karte.
        if skupljeno:
            self.__bodovi[i] += Tablic.vrijednostKarata({karta} | skupljeno) + int(skupljeno == stol) * Tablic.vrijednostTable()
            self.__skupljeno[i] += 1 + len(skupljeno)

            self.__zadnji = i

        # Azuriranje podataka o kartama koje i-ti igrac vjerojatno nema ako zadnje dijeljenje nije bilo posljednje u igri i ako i-ti igrac nije ovaj igrac.
        if self.__k and i != self.dohvatiIndeks():
            # Nakon sto je odigrao ovu kartu, nije poznato ima li i-ti igrac jos takvih karata.
            self.__vjerojatnoNema[i][PohlepniLog1.prevediKartu(karta)] = 0

            tudaRuka = MinimaxIgrac1.vjerojatnaRuka(self.__sigurnoNema, self.__vjerojatnoNema[i])
            # Ako igrac nije nista kupio sa stola, pregledavanje podigranih karata (znakova).
            podigrani = set()
            if not skupljeno:
                for x, Y in Tablic.moguciPotezi(stol | {karta}).items():
                    postoji = False
                    for y in Y:
                        if karta in y:
                            postoji = True

                            break
                    if postoji and not any(u.znak == x for u in tudaRuka):
                        podigrani |= {x}

            #if not skupljeno and not podigrani:
             #   for x, Y in Tablic.moguciPotezi(stol):
              #  	if len(Y) == 1:
               #         if Y[0] is Karta.Znak.BR2:
                #            self.__vjerojatnoNema[i][PohlepniLog1.prevediKartu(Karta(Karta.Boja.TREF, Karta.Znak.BR2))] += 1
                 #       elif Y[0] is Karta.Znak.BR10:
                  #  		self.__vjerojatnoNema[i][PohlepniLog1.prevediKartu(Karta(Karta.Boja.KARO, Karta.Znak.BR10))] += 1
                   #     self.__vjerojatnoNema[i][PohlepniLog1.prevediKartu(Karta(Y[0]))] += 1

            # Za svaku od podigranih karata umanjivanje vjerojatnosti da i-ti igrac nema tu kartu.
            #for x in podigrani:
             #   if x is Karta.Znak.BR2:
              #      self.__vjerojatnoNema[i][PohlepniLog1.prevediKartu(Karta(Karta.Boja.TREF, Karta.Znak.BR2))] -= 1
               # elif x is Karta.Znak.BR10:
                #    self.__vjerojatnoNema[i][PohlepniLog1.prevediKartu(Karta(Karta.Boja.KARO, Karta.Znak.BR10))] -= 1
                #self.__vjerojatnoNema[i][PohlepniLog1.prevediKartu(Karta(x))] -= 1

            # Racunanje vrijednosti odigranog poteza i karata koje i-ti igrac vjerojatno ima.
            vrijednost = (Tablic.vrijednostKarata(skupljeno | {karta}) if skupljeno else 0) + int(skupljeno == stol) * Tablic.vrijednostTable()
            tudaRuka = MinimaxIgrac1.vjerojatnaRuka(self.__sigurnoNema, self.__vjerojatnoNema[i])

            # Za svaki potez vrijedniji od odigranog, a koji ne zahtijeva igranje neke podigrane karte, uvecanje vrijednosti da igrac nema kartu kojom se taj potez igra.
            for potez in PohlepniIgrac1.izborPoteza(tudaRuka, stol):
                if potez['vrijednost'] + potez['tabla'] < vrijednost or (potez['vrijednost'] + potez['tabla'] == vrijednost and vrijednost > 0):
                    break
                elif (potez['vrijednost'] + potez['tabla'] == 0 and not podigrani and not skupljeno) or not potez['karta'].znak in podigrani:
                    self.__vjerojatnoNema[i][PohlepniLog1.prevediKartu(potez['karta'])] += 1

        

        # Azuriranje podataka o kartama koje igraci sigurno nemaju.
        self.__sigurnoNema |= {karta}

        # Ako je zadnje dijeljenje nije bilo posljednje u igri i ako je ostala samo jedna karta znaka odigrane karte u igri, pretpostavljanje da svi igraci imaju tu kartu.
        if self.__k and sum(int(x.znak == karta.znak) for x in self.__sigurnoNema) == 3:
            if karta.znak is Karta.Znak.BR2:
                k = PohlepniLog1.prevediKartu(Karta(Karta.Boja.TREF, Karta.Znak.BR2))
                for j in range(self.__n):
                    if j != self.dohvatiIndeks():
                        self.__vjerojatnoNema[j][k] = -Tablic.inicijalniBrojKarata_ruka()
            elif karta.znak is Karta.Znak.BR10:
                k = PohlepniLog1.prevediKartu(Karta(Karta.Boja.KARO, Karta.Znak.BR10))
                for j in range(self.__n):
                    if j != self.dohvatiIndeks():
                        self.__vjerojatnoNema[j][k] = -Tablic.inicijalniBrojKarata_ruka()
            k = PohlepniLog1.prevediKartu(Karta(karta.znak))
            for j in range(self.__n):
                if j != self.dohvatiIndeks():
                    self.__vjerojatnoNema[j][k] = -Tablic.inicijalniBrojKarata_ruka()

    def odigraj (self, ruka : set, stol : set, ponovi = False) -> tuple:
        """
        Minimax algoritmom pronadi najpovoljniji potez i odigraj ga.

        """

#       t0 = time.time()

        # Dohvati najvjerojatniji slijed poteza.
        grana = MinimaxIgrac1.minimax(copy.deepcopy(self.__sigurnoNema), copy.deepcopy(self.__vjerojatnoNema),
                                      ruka, stol,
                                      self.__bodovi, self.__skupljeno,
                                      self.__n, self.dohvatiIndeks(), self.dohvatiIndeks(),
                                      not self.__k, self.__zadnji,
                                      6 if not self.__k else self.__maxDubina, self.__maxT)

#       t1 = time.time()

#       print('{0:.3f} s'.format(float(t1 - t0)))

        if not grana:
            raise TypeError('Minimax algoritam nije pronasao nijedan moguci potez.')

        # Slucajnim odabirom odaberi kartu u ruci ekvivalentnu odabranoj minimax algoritmom.
        i = PohlepniLog1.prevediKartu(grana[0]['karta'])
        kandidati = []
        for x in ruka:
            if PohlepniLog1.prevediKartu(x) == i:
                kandidati.append(x)
        grana[0]['karta'] = random.choice(kandidati)

        # Odigraj najpovoljniji potez.
        return (grana[0]['karta'], grana[0]['skupljeno'])

    def bodovi (self) -> list:
        """
        Dohvati trenutno bodovno stanje.

        """

        return self.__bodovi

    def skupljeno (self) -> list:
        """
        Dohvati trenutno stanje broja skupljenih karata.

        """

        return self.__skupljeno

    def zadnji (self):
        """
        Dohvati informaciju o tome tko je zadnji kupio.

        """

        return self.__zadnji

    def sigurnoNema () -> set:
        """
        Dohvati trenutna saznanja o kartama koje drugi igraci sigurno nemaju.

        """

        return copy.deepcopy(self.__sigurnoNema)

    def vjerojatnoNema (i = None) -> list:
        """
        Dohvati trenutna saznanja o kartama koje drugi igraci vjerojatno nemaju.

        Ako i nije None, povratna vrijednost sukladna je argumentu vjerojatnoNema u
        funkciji MinimaxIgrac1.vjerojatna ruka, pri cemu nize vrijednosti predstavljaju
        vecu vjerojatnost da i-ti igrac ima tu kartu, a vise vrijednosti da nema (0 je
        neutralno, "mozda ima").  Ako je i None, onda je povratna vrijednost ugnjezdena
        lista kojoj je na k-tom mjestu lista koja bi se dobila pozivom
        self.vjerojatnoNema(k).

        """

        if i is None:
            return copy.deepcopy(self.__vjerojatnoNema)

        return copy.deepcopy(self.__vjerojatnoNema[i])
