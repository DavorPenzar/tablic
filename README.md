# tablic

Implementacija igre tablić i "robota igrača" za igru tablić

## Pravila igre *tablić*

**Napomena.** U ovoj implementaciji igre tablić koristi se poopćenje pravila te igre.

### Tip igre

Igra tablić društvena je kartaška igra koja se igra s jednim standardnim francuskim špilom karata bez *jokera* (4 boje i 13 znakova, to jest 52 karte).

### Broj igrača

Broj igrača mora biti djelitelj broja 48 strogo veći od 1.

**Napomena.** Igra se može smatrati kao igra skupina (na primjer, u 4 igrača kao jedan par igrača protiv drugog para igrača, kao u *beli* &mdash; prvi i treći protiv drugog i četvrtog), ali u ovoj implementaciji igra je relaizirana samo kao igra samostalnih igrača.

### Tijek igre

Prije početka partije ustanovljuje se redoslijed igrača (njihovih poteza) koji ostaje fiksan tijekom cijele partije.

Na početku partije postavljaju se 4 karte na stol (vidljive svima), a ostatak špila ostavlja se sa strane (tako da se preostale karte u špilu ne vide). Zatim se ponavljaju koraci:

1.  svim se igračima podijeli 6 karata ako je u špilu preostalo dovoljno karata, a inače se igračima karte u špilu ravnomjerno podijele; svaki igrač ima uvid samo u svoje karte i karte na stolu,
2.  igrajući u krug ustanovljenim redoslijedom igrača dok igrač koj treba biti na redu u ruci ima barem jednu kartu, svaki igrač igra potez tako da
    1.  iz svoje ruke bira kartu koju će odigrati,
    2.  ako ne može ili ne želi skupiti ništa sa stola, odigranu kartu odlaže na stol (ta karta ostaje na stolu i, kao i ostale karte na stolu, vidljiva je svim igračima), a inače preostalim igračima pokazuje odigranu kartu, sa stola skuplja sve skupove karata koji se mogu zbrojiti u odigranu kartu (v. *Pravila zbrajanja karata* dolje) tako da ti skupovi **nemaju zajedničkih karata** (kartom *pik 7* ne mogu se skupiti karte *herc 3*, *karo 4*, *tref 4* iako je *(herc) 3* + *(karo) 4* = *(pik) 7* i *(herc) 3* + *(tref) 4* = *(pik) 7* jer u tom slučaju karta *herc 3* sudjeluje u oba zbroja, ali mogu se skupiti karte *herc 3*, *pik 3*, *karo 4*, *tref 4* jer je *(herc) 3* + *(karo) 4* = *(pik) 7*, *(pik) 3* + *(tref) 4* = *(pik) 7* i skupovi {*herc 3*, *karo 4*}, {*pik 3*, *tref 4*} nemaju zajedničkih karata); ako je igrač skupio karte sa stola, odigranu kartu i karte skupljene sa stola sprema u svoj skup skupljenih karata (te karte više ne sudjeluju u igri),
3. kada nijedan igrač u svojoj ruci više nema karata, igra završava ako u špilu nije preostalo više karata, a inače se postupak ponavlja od koraka 1.

Na kraju partije, ako postoji igrač koji je zadnji skupio nešto sa stola, karte koje su preostale na stolu dodaju se skupu skupljenih karata tog igrača (koji je zadnji skupio nešto sa stola), ali to se **ne smatra ostvarivanjem table** (v. *Ostvarivanje* table dolje).

### Pravila zbrajanja karata

Tijekom igre, svaka karta ima svoju numeričku vrijednost (neovisnu o bodovnoj vrijednosti kod računanja ostvarenih bodova igrača; v. *Bodovanje* dolje). Pri skupljanju karata sa stola, poenta je da se numeričke vrijednosti skupljenih karata sa stola mogu zbrojiti u numeričku vrijednost odigrane karte.

Numeričke vrijednosti karata iznose:

*   za brojeve onoliko koliki je broj (npr. numerička vrijednost karte *herc 5* je 5, a karte *tref 8* je 8),
*   za *J* 12, za *Q* 13 i za *K* 14,
*   za *A* 1 ili 11 (kako igrač pri skupljanju želi i kako mu odgovara).

Na primjer, kartom *karo J* može se skupiti:

*   *tref J* (12 = 12),
*   *pik 2*, *tref 10* (2 + 10 = 12),
*   *karo 2*, *karo 3*, *herc 7* (2 + 3 + 7 = 12),
*   *pik A*, *herc 3*, *pik 3*, *tref 5* (1 + 3 + 3 + 5 = 12),
*   *herc A*, *tref A* (1 + 11 = 12).

Štoviše, kako nijedne dvije od gore spomenutih varijanti ne sadrže nijednu istu kartu, u teoriji je sve spomenute karte moguće odjednom skupiti sa stola (u praksi je, međutim, malo vjerojatno da će u nekom trenutku stol biti toliko *bogat* da će odjednom biti svih 5 kombinacija na stolu).

Osim što više karata znaka *A* pri zbrajanju mogu imati različite vrijednosti (kao što je gore *(herc) A* + *(tref) A* = *(karo) J*), isto tako različite vrijednosti karata znaka *A* mogu se pojavljivati i s *različitih strana jednakosti*, to jest kartom *pik A* može se skupiti:

*   *herc A* (1 = 1 ili 11 = 11),
*   *herc A*, *tref 10* (1 + 10 = 11),
*   *herc A*, *karo A*, *pik 9* (1 + 1 + 9 = 11),
*   *herc A*, *karo A*, *tref A*, *herc 8* (1 + 1 + 1 + 8 = 11).

### Bodovanje

Cilj je svakog igrača skupiti što veći broj bodova. U stvari, igra se obično igra tako da se igra više partija za redom, i to tako da, na prmijer, igrači X, Y, Z u partijama izmjenjuju redoslijede poteza (X, Y, Z), (Y, Z, X), (Z, X, Y), &hellip;, a skupljeni bodovi se u partijama zbrajaju, i konačni je pobjednik onaj koji je ukupno skupio najveći broj bodova (a ne nužno onaj koji je u najviše partija imao najveći broj bodova).

Osnovni broj bodova svakog igrača zbroj je bodovnih vrijednosti svih karata u njegovom skupu skupljenih karata. Na taj se broj nadodaje još broj ostvarenih tabli tijekom partije (v. *Ostvarivanje* table dolje) i, ako postoji igrač koji je skupio strogo najveći broj karata, njemu se još dodaju 3 boda (ako su dva ili više igrača skupili najviše karata, nikome se ne dodjeljuju ti dodatni bodovi).

Bodovne vrijednosti karata iznose:

*   sve karte brojeva osim broja 10 i osim karte *tref 2* vrijede 0 bodova,
*   sve ostale karte osim karte *karo 10* vrijede 1 bod,
*   karta *karo 10* vrijedi 2 boda.

Zbroj bodovnih vrijednosti svih karata u igri iznosi 22, stoga bez tabli zbroj bodova svih igrača u jednoj partiji iznosi 22 ili 25 (ako postoji igrač koji je skupio strogo najveći broj bodova, što vrijedi 3 boda, onda je zbroj svih bodova 22 + 3 = 25).

#### Ostvarivanje *table*

Tijekom igre, svaki put kada neki igrač odigranom kartom skupi sve karte sa stola, taj mu se čin smatra ostvarivanjem table, što zapravo znači da je osvojio još jedan dodatni bod (bod koji ne ulazi u ranije spomenutu sumu bodova tijekom partije koja iznosi 22 odnosno 25). Naravno, kako svaki igrač, kada je na potezu, mora odigrati neku kartu iz ruke, igrač koji je na potezu neposredno nakon igrača koji je ostvario tablu odigranu kartu može jedino odložiti na stol (na stolu ne postoje karte koje bi se odigranom kartom mogle skupiti).

## Datoteke

Kompletna implementacija igre napisana je objektno orijentirano u programskom jeziku Python.

1.  **skupovi.py** &ndash; implementacija nekih skupovnih operacija korisnih za implementaciju igre tablić,
2.  **karta.py** &ndash; implementacija klase `Karta` za reprezentaciju karata u igri tablić,
3.  **engine.py** &ndash; implementacija klase `Tablic` za simulaciju igranja igre tablić, apstraktnih klasa `Tablic.Log` i `Tablic.Igrac` kao prototipa klasa zapisnika partija i igrača igre respektivno, i klasa `Tablic.PrazniLog` i `Tablic.RandomIgrac` kao najjednostavnijih neapstraktnih proširenja apstraktnih klasa `Tablic.Log` i `Tablic.Igrac` (zapisnik koji ne zapisuje ništa i igrač koji igra slučajnim odabirom),
4.  **pohlepni_log.py** &ndash; implementacija klase zapisnika igre tablić za strojno učenje pohlepnog algoritma,
5.  **minimax_log.py** &ndash; implementacija klase zapisnika igre tablić za strojno učenje minimax algoritma,
6.  **pohlepni_igrac.py** &ndash; implementacija klase igrača igre tablić koji igra pohlepnim algoritmom,
7.  **minimax_igrac.py** &ndash; implementacija klase igrača igre tablić koji igra minimax algoritmom,
8.  **io_igrac.py** &ndash; implementacija klase `IOIgrac` za *stdin*/*stdout* igrača igre tablić,
9.  **promatrac_log.py** &ndash; implementacija klase `PromatracLog` koji ispisuje tijek igre na *stdout*,
10. **usporedba.py** &ndash; skripta za testiranje igrača igre tablić.

Svi bi kodovi trebali biti kompatibilni za Python2 i Python3 sa standardnom bibliotekom. Detaljnije informacije o implementiranim klasama i funkcijama dane su u *inline* dokumentaciji i komentarima. Argumenti funkcija gotovo nigdje nisu provjeravani i sanirani radi preglednosti koda i neznatnog ubrzanja, a ispravno služenje kodom ne će izazivati probleme.

## Algoritmi

### Pohlepni algoritam

Igrač koji igra pohlepnim algoritmom (`PohlepniIgrac`) u svakom potezu pokušava maksimalizirati trenutni dobitak (prvenstveno broj bodova, a zatim i broj skupljenih karata; ako može, ostvarit će tablu), a, ako ne može ništa skupiti, na stol odlaže kartu najmanje numeričke vrijednosti osim *A* (i osim *tref 2* i *karo 10*) zato što je vjerojatnije da će se karte većih numeričkih vrijednosti lakše složiti na stolu u daljnjem tijeku igre. Također, kada su dva poteza jednako vrijedna, iz istih razloga bira onaj kojim kupi kartu s manjom numeričkom vrijednosti. Karte znaka *A* i karte *tref 2* i *karo 10* pokušava ne odlagati na stol, ali isto tako one imaju prioritet pri skupljanju sa stola (i kao karte kojom igra i kao karte koje se sa stola uzimaju), pri čemu je karta *karo 10* najvećeg prioriteta, zatim *tref 2* i zatim sve karte znaka *A* (pri odlaganju na stol bez skupljanja karata redoslijed kojim ih *radije* odlaže je obratan).

### Minimax algoritam

Iako igra tablić nije zapravo pogodna za minimax algoritam jer su informacije skrivene (igrači nemaju uvid u tuđe karte u rukama), igrač `MinimaxIgrac` implementiran je tako da o potezima odlučuje adaptiranim minimax algoritmom. Adaptacija minimax algoritma je takva da se neke grane stabla poteza odbacuju pod pretpostavkom da nisu vjerojatne ili da ne će doprinjeti odluci. Prvenstveno, igrač pamti koje karte drugi igrači sigurno nemaju (inicijalne karte na stolu, karte koje on ima u ruci i karte koje su drugi igrači igrali), ali također pretpostavlja koje karte pojedini igrači vjerojatno nemaju s obzirom na način na koji igraju. Sam minimax algoritam ovdje implementiran na sličan način za dublje razine *pretpostavlja* koje karte igrači vjerojatno nemaju ako se u nekoj plićoj razini razmatra određeni potez. Također, kako minimax algoritam poteze provjerava redoslijedom kojim ih pohlepni igrač sortira, u završnim dubinama pretraživanje poteza se prekida kada igraču čiji se potezi u toj razini razmatraju heurističke vrijednosti poteza počinju biti lošije (kada max-igraču počinju opadati i kad min-igraču počinju rasti) pod pretpostavkom da će i *lošiji* potezi (lošiji u smislu pohlepnog algoritma) dati još lošije heurističke vrijednosti. Uz sve to, minimax algoritam implementiran je s alpha/beta-podrezivanjem.

Heuristička vrijednost lista stabla poteza uređeni je par `(heurBodovi, heurSkupljeno)`, gdje je `heurBodovi` razlika bodova max-igrača i aritmetičke sredine bodova svih min-igrača, a `heurSkupljeno` razlika broja skupljenih karata max-igrača i aritmetičke sredine broja skupljenih karata svih min-igrača. Naravno, ako je stanje igre završno, prije računanja tih vrijednosti čine se koraci na kraju igre (karte sa stola pribrajaju se skupljenim kartama igrača koji je zadnji kupio sa stola i traži se igrač sa strogo najvećim brojem skupljenih karata). Heurističke vrijednosti u obliku uređenih parova uspoređuju se leksikografski. Ipak, zbog načina na koje je stablo poteza *podrezano*, prvi argument po kojem se potezi uspoređuju je taj da se uzima onaj potez čiji list je dublje u stablu (potez čija je heuristička vrijednost relevantnija jer je izračunata na temelju većeg broja informacija), neovisno o odnosu heurističkih vrijednosti poteza.

Stablo poteza pretražuje se DFS-om, a dubina stabla zadaje najveći broj poteza max-igrača koji će se provjeravati i to tako da su u listovima stabla svi igrači odigrali jednaki broj poteza. Na primjer, ako je promatrani minimax igrač prvi na potezu u igri za 2 igrača i ako je zadana maksimalna dubina stabla 3 (i ako on u promatranom trenutku ima barem 3 karte u ruci), dubina stabla bit će zapravo 6: on (1/3), suparnik, on (2/3), suparnik, on (3/3), suparnik. U sličnom scenariju, ali tako da je minimax igrač drugi na potezu, dubina stabla će biti 5 jer je prije pretraživanja stabla njegov suparnik odigrao jedan potez više od njega: on (1/3), suparnik, on (2/3), suparnik, on (3/3). Listovima stabla uzimaju se stanja igre u kojima bi u idućem potezu trebao biti igrač koji je u krugu poteza prvi na potezu, a max-igrač više nema karata u ruci (to zapravo znači da su svi igrači odigrali sve karte u ruci, a minimax algoritam ne pregledava moguću iduću ruku max-igrača zbog prevelikog stupnja grananja). Isto tako, listovi su stanja u kojima, zbog previše pretpostavki, min-igrač koji bi trebao biti na redu *nema* kartu koju bi mogao igrati (za sve karte se zna da ih sigurno nema ili se pretpostavlja da ih nema). Nakon posljednjeg dijeljenja u partiji, međutim, dubina se uvijek uzima maksimalna moguća (metoda `MinimaxIgrac.minimax` dopušta plića stabla nakon zadnjeg dijeljenja, ali metoda `MinimaxIgrac.odigraj` nakon zadnjeg dijeljenja metodu `MinimaxIgrac.minimax` poziva s dubinom `Tablic.inicijalniBrojKarata_ruka()`)

Još jedna nekonvencionalna preinaka minimax algoritma vremensko je ograničenje. Naime, kako se potezi razmatraju redoslijedom kojim ih pohlepni algoritam sortira, vjerojatnije je da će max-igraču i min-igračima više odgovarati potezi koji generiraju *lijeve* grane stabla pa se zbog brzine odluke može zadati maksimalno dopušteno vrijeme za pretraživanje stabla pod pretpostavkom da je nakon dovoljno vremena najbolji potez pronađen iako nije pretraženo cijelo stablo. Ipak, to vremensko ograničenje može se postaviti i na pozitivnu beskonačnost (`float('inf')`) što zapravo znači da vremenskog ograničenja nema.

Način na koji se pretpostavlja da neki igrač nema neku kartu je takav da se njegov potez uspoređuje sa svim potezima koje bi mogao učiniti s kartama za koje nije poznato da ih sigurno nema i za koje se ne pretpostavlja da ih vjerojatno nema. Pretpostavlja se da igrač nema sve karte (osim onih koje su ekvivalentne numeričke i bodovne vrijednosti kao odigrana karta) koje omogućuju igranje poteza sa strogo većom bodovnom vrijednosti ili s jednakom bodovnom vrijednosti, ali sa skupljanjem strogo većeg broja karata sa stola. Pri svakom dijeljenju sve se prethodne pretpostavke zanemaruju, a nakon zadnjeg dijeljenja takve se pretpostavke više ne izvode (ako igraju 2 igrača, u potpunosti je poznato koje karte suparnik ima, a i u partijama s više igrača sigurnije je tako zbog dodanih vrijednosti na kraju igre).

## Testiranje igrača

Igrači se mogu testirati pokretanjem skripte *usporedba.py*. Skripta je napisana vrlo *algoritamski*, to jest dovoljne su minimalne promjene nekih varijabli na početku skripte (na primjer, broj partija) za postizanje drugačijih rezultata. Elementi *tuple*-a igrača rječnici su s ključevima *klasa* (klasa čija će instanca biti taj igrač), *args* (*tuple* argumenata za inicijalizaciju igrača), *kwargs* (rječnik argumenata zadanih ključnom rječju za inicijalizaciju igrača). Igrač se inicijalizira pozivom `igrac['klasa'](i, *igrac['args'], **igrac['kwargs'])` (redni broj igrača `i` u partiji određuje objekt klase `Tablic`). Redoslijed igrača u *tuple*-u igrača zadaje red kojim su na potezu, osim ako se skripta ne pokreče kao `./usporedba.py -r` (uzima se obrnuti redsolijed) ili ` ./usporedba.py -p` (uzima se slučajni redoslijed). Ispis programa objašnjen je u komentarima u skripti *usporedba.py*.

### Igranje protiv automatskih igrača

Igranje protiv *robota* igrača moguće je dodavanjem igrača klase `IOIgrac` u igru u skripti *usporedba.py* i pokretanjem te skripte. S obzirom na to da se ispis kod `IOIgrac`-a vrši na *stdout*, a, između ostalog, igraču se ispisuju karte koje ima u ruci, s trenutnom implementacijom nije izvediva poštena partija između 2 *ljudska* igrača.

#### Zadavanje poteza

Potezi se zadaju pisanjem na *stdin*. Pri određivanju karte koju se želi igrati ili skupiti sa stola, najjednostavnije je pisati (mogući su razni oblici zadavanja karte, ali ovaj je najjasniji)

*   *a* za kartu znaka A,
*   broj karte broja,
*   *j*, *q*, *k* za karte znakova *J*, *Q*, *K* respektivno.

Naravno, unos nije *case-sensitive* (ekvivalentno je pisati *a* i *A*). Posebno određivanje boje karte moguće je pisanjem *tref 2* umjesto *2*, ali, osim u slučajevima karata *tref 2* i *karo 10*, boja karte nije bitna. Ako igrač ima barem dvije karte znaka *2* u ruci od kojih je jedna *tref 2* i ako napiše *2* kao kartu koju želi igrati, bit će upitan želi li igrati *tref 2* ili ne; ako ima samo kartu *tref 2* od karata znaka *2* ili ako kartu *tref 2* nema, upita o igranju karte *tref 2* ne će biti. S druge strane, ako je na stolu više karata znaka *2* i ako igrač napiše kao kartu koju želi skupiti sa stola *2*, prvo se uzima *tref 2*, a tek nakon nje i ostale (ako se želi skupiti više karata istog znaka, ne nužno *2*, sa stola, potrebno je toliko puta napisati taj znak koliko se tih karata želi skupiti). Sve ovo nalogno vrijedi i u slučaju karata znaka *10* i istaknute karte *karo 10*. Unosi se odvajaju **samo** prelaskom u novi red (bez zareza), a kraj skupljanja karata sa stola označava se praznim unosom.

U svakom trenutku pri biranju karata za skupiti sa stola moguće je napisati *auto* (također nije *case-sensitive*) pri čemu se bira potez kojeg bi pohlepni igrač s odigranom kartom igrao. Međutim, ako su na stolu, na primjer, karte *herc 4*, *herc 6*, *tref 10*, *karo A*, ako igrač igra kartu *pik A* i ako je za skup skupljenih karata pisao redom *6*, *auto*, sa stola će se uzeti *herc 4*, *herc 6*, *karo A* jer se u tom slučaju uzima karta znaka *6* sa stola iako bi pohlepni igrač s kartom *pik A* uzimao *tref 10*, *karo A*. Efekt stvarnog igranja poteza po izboru pohlepnog igrača postiže se tako da se napiše samo *auto*, bez zadavanja konkretnih karata prije (karte koje se eventualno zadaju prije pisanja *auto* nužno se uzimaju, a tek se povrh njih bira *najbogatiji* potez). Mogućnost pisanja *auto* ne bi se smijela *zloupotrebljavati* (previše koristiti) jer se time gubi smisao igranja igre kao čovjek: moguće je da igrač nije primijetio trenutno i beskontekstno najbolji potez, ali je unosom *auto* ipak skupio najbolji mogući skup karata sa stola, što stvarnim igranjem igre tablić papirnatim kartama ne bi mogao osim uz dobronamjernu intervenciju suigrača.
