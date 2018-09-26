# tablic

Implementacija igre tablić i "robota igrača" za igru tablić

## Pravila igre *tablić*

**Napomena.** U ovoj implementaciji igre tablić koristi se poopćenje pravila te igre.

### Tip igre

Igra tablić društvena je kartaška igra koja se igra sa standardnim francuskim špilom karata bez *jokera*.

### Broj igrača

Broj igrača mora biti djelitelj broja 48 strogo veći od 1.

**Napomena.** Igra se može smatrati kao igra skupina (na primjer, u 4 igrača kao jedan par protiv drugog para), ali u ovoj implementaciji igra je relaizirana samo kao igra samostalnih igrača.

### Tijek igre

Prije početka partije ustanovljuje se redoslijed igrača (njihovih poteza) koji ostaje fiksan tijekom cijele partije.

Na početku partije postavljaju se 4 karte na stol (vidljive svima), a ostatak špila ostavlja se sa strane (tako da se preostale karte u špilu ne vide). Zatim se ponavljaju koraci:

1. svim se igračima podijeli 6 karata ako je u špilu preostalo dovoljno karata, a inače se igračima karte u špilu ravnomjerno podijele; svaki igrač ima uvid samo u svoje karte i karte na stolu,
2. ustanovljenim redoslijedom igrača, svaki igrač igra potez tako da
    1. iz svoje ruke bira kartu koju će odigrati,
    2. ako ne može ili ne želi skupiti ništa sa stola, odigranu kartu odlaže na stol (ta karta ostaje na stolu i, kao i ostale karte na stolu, vidljiva je svim igračima), a inače preostalim igračima pokazuje odigranu kartu, sa stola skuplja sve skupove karata koji se mogu zbrojiti u odigranu kartu (v. *Pravila zbrajanja karata* dolje) tako da ti skupovi **nemaju zajedničkih karata** (kartom *pik 7* ne mogu se skupiti karte *herc 3*, *karo 4*, *tref 4* iako je *(herc) 3* + *(karo) 4* = *(pik) 7* i *(herc) 3* + *(tref) 4* = *(pik) 7* jer u tom slučaju karta *herc 3* sudjeluje u oba zbroja, ali mogu se skupiti karte *herc 3*, *pik 3*, *karo 4*, *tref 4* jer je *(herc) 3* + *(karo) 4* = *(pik) 7*, *(pik) 3* + *(tref) 4* = *(pik) 7* i skupovi {*herc 3*, *karo 4*}, {*pik 3*, *tref 4*} nemaju zajedničkih karata); ako je igrač skupio karte sa stola, odigranu kartu i karte skupljene sa stola sprema u svoj skup skupljenih karata (te karte više ne sudjeluju u igri),
3. kada nijedan igrač u svojoj ruci više nema karata, igra završava ako u špilu nije preostalo više karata, a inače se postupak ponavlja od koraka 1.

Na kraju partije, ako postoji igrač koji je zadnji skupio nešto sa stola, karte koje su preostale na stolu dodaju se skupu skupljenih karata tog igrača (koji je zadnji skupio nešto sa stola), ali to se **ne smatra ostvarivanjem table** (v. *Ostvarivanje* table dolje).

### Pravila zbrajanja karata

Tijekom igre, svaka karta ima svoju numeričku vrijednost (neovisnu o bodovnoj vrijednosti kod računanja ostvarenih bodova igrača; v. *Bodovanje* dolje). Pri skupljanju karata sa stola, poenta je da se numeričke vrijednosti skupljenih karata sa stola mogu zbrojiti u numeričku vrijednost odigrane karte.

Numeričke vrijednosti karata iznose:

* za brojeve onoliko koliki je broj (npr. numerička vrijednost karte *herc 5* je 5, a karte *tref 8* je 8),
* za *J* 12, za *Q* 13 i za *K* 14,
* za *A* 1 ili 11 (kako igrač pri skupljanju želi i kako mu odgovara).

Na primjer, kartom *karo J* može se skupiti:

* *tref J* (12 = 12),
* *pik 2*, *tref 10* (2 + 10 = 12),
* *karo 2*, *karo 3*, *herc 7* (2 + 3 + 7 = 12),
* *pik A*, *herc 3*, *pik 3*, *tref 5* (1 + 3 + 3 + 5 = 12),
* *herc A*, *tref A* (1 + 11 = 12).

Štoviše, kako nijedne dvije od gore spomenutih varijanti ne sadrže nijednu istu kartu, u teoriji je sve spomenute karte moguće odjednom skupiti sa stola (u praksi je, međutim, malo vjerojatno da će u nekom trenutku stol biti toliko *bogat* da će odjednom biti svih 5 kombinacija na stolu).

Osim što više karata znaka *A* pri zbrajanju mogu imati različite vrijednosti (kao što je gore *(herc) A* + *(tref) A* = *(karo) J*), isto tako različite vrijednosti karata znaka *A* mogu se pojavljivati i s *različitih strana jednakosti*, to jest kartom *pik A* može se skupiti:

* *herc A* (1 = 1 ili 11 = 11),
* *herc A*, *tref 10* (1 + 10 = 11),
* *herc A*, *karo A*, *pik 9* (1 + 1 + 9 = 11),
* *herc A*, *karo A*, *tref A*, *herc 8* (1 + 1 + 1 + 8 = 11).

### Bodovanje

Cilj je svakog igrača skupiti što veći broj bodova. U stvari, igra se obično igra tako da se igra više partija za redom, i to tako da igrači X, Y, Z u partijama izmjenjuju redoslijede poteza (X, Y, Z), (Y, Z, X), (Z, X, Y), ..., a skupljeni bodovi se u partijama zbrajaju, i konačni je pobjednik onaj koji je ukupno skupio najveći broj bodova (a ne nužno onaj koji je u najviše partija imao najveći broj bodova).

Osnovni broj bodova svakog igrača zbroj je bodovnih vrijednosti svih karata u njegovom skupu skupljenih karata. Na taj se broj nadodaje još broj ostvarenih tabli tijekom partije (v. *Ostvarivanje* table dolje) i, ako postoji igrač koji je skupio strogo najveći broj karata, njemu se još dodaju 3 boda (ako su dva ili više igrača skupili najviše karata, nikome se ne dodjeljuju ti dodatni bodovi).

Bodovne vrijednosti karata iznose:

* sve karte brojeva osim broja 10 i osim karte *tref 2* vrijede 0 bodova,
* sve ostale karte osim karte *karo 10* vrijede 1 bod,
* karta *karo 10* vrijedi 2 boda.

Zbroj bodovnih vrijednosti svih karata u igri iznosi 22, stoga bez tabli zbroj bodova svih igrača u jednoj partiji iznosi 22 ili 25 (ako postoji igrač koji je skupio strogo najveći broj bodova, što vrijedi 3 boda, onda je zbroj svih bodova 22 + 3 = 25).

#### Ostvarivanje *table*

Tijekom igre, svaki put kada neki igrač odigranom kartom skupi sve karte sa stola, taj mu se čin smatra ostvarivanjem table, što zapravo znači da je osvojio još jedan dodatni bod (bod koji ne ulazi u ranije spomenutu sumu bodova tijekom partije koja iznosi 22 odnosno 25). Naravno, kako svaki igrač kada je na potezu mora odigrati neku kartu iz ruke, igrač koji je na potezu neposredno nakon igrača koji je ostvario tablu odigranu kartu može jedino odložiti na stol (na stolu ne postoje karte koje bi se odigranom kartom mogle skupiti).

## Datoteke

1. **skupovi.py** -- implementacija nekih skupovnih operacija korisnih za implementaciju igre tablić,
2. **karta.py** -- implementacija klase `Karta` za reprezentaciju karata u igri tablić,
3. **engine.py** -- implementacija klase `Tablic` za simulaciju igranja igre tablić,
4. **pohlepni_log.py** -- implementacija klasa zapisnika igre tablić za strojno učenje pohlepnih algoritama,
5. **pohlepni_igrac.py** -- implementacija klasa igrača igre tablic koji igraju pohlepnim algoritmom,
6. **io_igrac.py** -- implementacija klase `IOIgrac` za *stdin*/*stdout* igrača igre tablić,
7. **minimax_igrac.py** -- implementacija klasa igrača igre tablić koji igraju minimax algoritmom,
8. **minimax_log.py** -- implementacija klasa zapisnika igre tablić za strojno učenje minimax algoritama.
