# -*- coding: utf-8 -*-

"""
Implementacija nekih skupovnih operacija.

"""

def partitivniSkup (S):
    """
    Izracunaj partitivni skup (konacnog) skupa S.

    Partitivni skup skupa S racuna se na nacin:
        1.  Inicijaliziramo partitivni skup na P = {{}} (prazni skup je podskup
            svakog skupa).
        2.  Iteriramo po svim elementima (x) skupa S.  Kako su svi dosadasnji
            skupovi u P disjunktni s {x}, za svaki A u P novi poznati podskup
            od S je A unija {x} --- stoga A unija X dodajemo u P.
    Slozenost funkcije je stoga eksponencijalna, reda O(2^n), gdje je n ukupni
    broj svih (razlicitih) elemenata u S.

    Elementi povratnog skupa P (objekt klase set) objekti su klase frozenset
    ciji se svi elementi nalaze u S.  Za svaku kolekciju nekih elemenata iz S
    postoji jedinstveni skup u P koji sadrzi te i samo te elemente iz S.

    """

    # Inicijaliziraj partitivni skup na {{}}.
    P = {frozenset()}

    # Konstruiraj partitivni skup skupa S.
    for x in S:
        Q = set()
        for A in P:
            Q |= {frozenset(A | {x})}
        P |= Q

    # Vrati izracunati partitivni skup.
    return P

def unijeDisjunktnih (F):
    """
    Izracunaj familiju svih unija disjunktnih elemenata konacne familije F.

    Uniju u parovima disjunktnih elemenata familije F definiramo kao uniju svih
    skupova u nekoj podfamiliji G familije F tako da za svake X, Y u G je X = Y
    ili su X, Y disjunktni skupovi.  G ocito moze biti i prazni skup ili
    jednoclani skup, stoga je kardinalitet povratne familije barem card(F) + 1
    (cak i ako je F prazna familija).

    Familija svih unija u parovima disjunktnih elemenata familije F racuna se
    na nacin:
        1.  Inicijaliziramo familiju U unija u parovima disjunktnih elemenata
            familije F na {{}}.
        2.  Iteriramo po svim elementima (S) familije F.  Za svaki A iz U takav
            da su A i S disjunktni A unija S nova je poznata unija u parovima
            disjunktnih elemenata familije F --- stoga A unija S dodajemo u U.
    Slozenost funkcije je stoga reda O(2^n * k), gdje su n ukupni broj svih
    (razlicitih) elemenata u F i k zbroj kardinaliteta svih elemenata familije
    F.  Prethodna ocjena pociva na pretpostavci da je slozenost funkcije
    set.isdisjoint(X, Y) linearne slozenosti min/max({card(X), card(Y)}).

    Elementi povratne familije U (objekt klase set) objekti su klase frozenset.
    Za svaki A iz U postoji podfamilija G = {X1, X2, ..., Xm} familije F takva
    da za svake i, j iz {1, 2, ..., m} je Xi != Xj ako je i != j i da vrijedi
    A = X1 unija X2 unija ... unija Xm.  Vrijedi i obrat (za svaku takvu
    podfamiliju G postoji takav A).

    """

    # Inicijaliziraj familiju unija u parovima disjunktnih elemenata familije
    # F na {{}}.
    U = {frozenset()}

    # Konstruiraj familiju unija u parovima disjunktnih elemenata familije F.
    for S in F:
        S = frozenset(S)

        V = set()
        for A in U:
            if A.isdisjoint(S):
                V |= {frozenset(A | S)}
        U |= V

    # Vrati familiju unija u parovima disjunktnih elemenata familije F.
    return U
