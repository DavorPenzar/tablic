"""
Implementacija nekih skupovnih operacija korisne za implementaciju igre tablic.

"""

def partitivniSkup (S):
    """
    Izracunaj partitivni skup (konacnog) skupa S.

    Partitivni skup skupa S racuna se na nacin:
        1.  Inicijaliziramo partitivni skup na P = {{}} (prazni skup je podskup
            svakog skupa).
        2.  Iteriramo po svim elementima (x) skupa S.  Kako su svi dosadasnji
            skupovi u P disjunktni s {x}, za svaki A u P novi poznati podskup od S
            je A unija {x} --- stoga A unija X dodajemo u P.
    Slozenost funkcije je stoga eksponencijalna, reda O(2^n), gdje je n ukupni broj
    svih (razlicitih) elemenata u S.

    Parameters
    ----------
    S : set
        Konacni skup ciji se partitivni skup racuna.

    Returns
    -------
    P : set
        Elementi povratnog skupa P objekti su klase frozenset ciji se svi elementi
        nalaze u S.  Za svaku kolekciju nekih elemenata iz S postoji jedinstveni
        skup u P koji sadrzi te i samo te elemente iz S.

    Raises
    ------
    TypeError
        Ako (eventualno potrebna) konverzija objekta S u objekt klase set rezultira
        iznimkom klase TypeError ili ValueError, izbacuje se iznimka klase
        TypeError.

    Examples
    --------
    >>> partitivniSkup({0, 1, 2})
    set([frozenset([0]), frozenset([1, 2]), frozenset([]), frozenset([0, 2]), frozenset([1]), frozenset([0, 1, 2]), frozenset([2]), frozenset([0, 1])])
    >>> partitivniSkup(set())
    set([frozenset([])])

    """

    # Sanacija argumenta ako je potrebna.
    if not isinstance(S, set):
        try:
            S = set(S)
        except (TypeError, ValueError):
            raise TypeError("S mora biti skup (objekt klase `set').")

    # Inicijalizacija partitivnog skupa na {{}}.
    P = {frozenset()}

    # Konstrukcija partitivnog skupa skupa S.
    for x in S:
        Q = set()
        for A in P:
            Q |= {frozenset(A | {x})}
        P |= Q

    # Vracanje izracunatog partitivnog skupa.
    return P

def unijeDisjunktnih (F):
    """
    Izracunaj familiju svih unija u parovima disj. elemenata konacne familije F.

    Uniju u parovima disjunktnih elemenata familije F definiramo kao uniju svih
    skupova u nekoj podfamiliji G familije F tako da za svake X, Y u G je X = Y ili
    su X, Y disjunktni skupovi.  G ocito moze biti i prazni skup ili jednoclani
    skup, stoga je kardinalitet povratne familije barem card(F) + 1 (cak i ako je F
    prazna familija).

    Familija svih unija u parovima disjunktnih elemenata familije F racuna se na
    nacin:
        1.  Inicijaliziramo familiju U unija u parovima disjunktnih elemenata
            familije F na {{}}.
        2.  Iteriramo po svim elementima (S) familije F.  Za svaki A iz U takav da
            su A i S disjunktni A unija S nova je poznata unija u parovima
            disjunktnih elemenata familije F --- stoga A unija S dodajemo u U.
    Slozenost funkcije je stoga reda O(2^n * k), gdje su n ukupni broj svih
    (razlicitih) elemenata u F i k zbroj kardinaliteta svih elemenata familije F.
    Prethodna ocjena pociva na pretpostavci da je slozenost funkcije
    set.isdisjoint(X, Y) linearne slozenosti min/max({card(X), card(Y)}).

    Parameters
    ----------
    F : set
        Konacna familija skupova cija se familija svih unija u parovima disjunktnih
        elemenata racuna.  Svi elementi familije F trebali bi biti konvertibilni u
        objekt klase frozenset.

    Returns
    -------
    U : set
        Elementi povratne familije F objekti su klase frozenset.  Za svaki A iz U
        postoji podfamilija G = {X1, X2, ..., Xm} familije F takva da za svake i, j
        iz {1, 2, ..., m} je Xi != Xj ako je i != j i da vrijedi A = X1 unija X2
        unija ... unija Xm.  Vrijedi i obrat (za svaku takvu podfamiliju G postoji
        takav A).

    Raises
    ------
    TypeError
        Ako (eventualno potrebna) konverzija objekta S u objekt klase set rezultira
        iznimkom klase TypeError ili ValueError, izbacuje se iznimka klase
        TypeError.  Takoder, ako konverzija bilo kojeg elementa familije F u objekt
        klase frozenset rezultira iznimkom tipa TypeError ili ValueError, izbacuje
        se iznimka klase TypeError.

    Examples
    --------
    >>> unijeDisjunktnih({frozenset({0}), frozenset({1})})
    set([frozenset([1]), frozenset([]), frozenset([0]), frozenset([0, 1])])
    >>> unijeDisjunktnih({frozenset({0, 1}), frozenset({1}), frozenset({2}), frozenset({1, 3})})
    set([frozenset([1, 2]), frozenset([0, 1, 2]), frozenset([1]), frozenset([1, 3]), frozenset([2]), frozenset([1, 2, 3]), frozenset([]), frozenset([0, 1])])
    >>> unijeDisjunktnih(set())
    set([frozenset([])])

    """

    if not isinstance(F, set):
        try:
            F = set(F)
        except (TypeError, ValueError):
            raise TypeError("F mora biti skup (objekt klase `set').")

    U = {frozenset()}

    for S in F:
        try:
            S = frozenset(S)
        except (TypeError, ValueError):
            raise TypeError("Elementi familije F moraju biti skupovi (objekti "
                            "klase `frozenset').")

        V = set()
        for A in U:
            if A.isdisjoint(S):
                V |= {frozenset(A | S)}
        U |= V

    return U
