#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
Skripta za igranje protiv robotskih igraca igre tablic.

"""

import math
import random
import six
import sys
import time

from engine import Tablic
from pohlepni_log import PohlepniLog
from minimax_log import MinimaxLog
from pohlepni_igrac import PohlepniIgrac
from minimax_igrac import MinimaxIgrac
from io_igrac import IOIgrac
from promatrac_log import PromatracLog

# Igraci koji ce se testirati.  Redoslijed igraca zadaje redoslijed kojim ce
# biti na potezu u partijama (osim ako se skripta ne pozove s argumentom koji
# mijenja redoslijed igraca, ali ne i skup igraca).  Svaki igrac reprezentiran
# je rjecnikom s kljucevima 'klasa', 'args', 'kwargs', a dodaju se u igru
# pozivom
#     >>> igra.dodajIgraca(igrac['klasa'], *igrac['args'], **igrac['kwargs'])
igraci = ({'klasa' : IOIgrac, 'args' : tuple(), 'kwargs' : {'ime' : 'Andrej'}},
          {'klasa' : MinimaxIgrac, 'args' : tuple(), 'kwargs' : {'ime' : 'Marconi', 'maxDubina' : 3, 'maxT' : 15.0}})

# Ako je pri pokretanju skripte zadan argument "-r", redoslijed igraca u tuple-u igraci se obrce.  Ako je zadan argument "-p", redoslijed igraca permutira
# se slucajnim izborom.  Ostali dodatni argumenti se ne prepoznaju.
if len(sys.argv) == 2:
    if sys.argv[1] == '-r':
        igraci = tuple(reversed(igraci))
    elif sys.argv[1] == '-p':
        igraci = list(igraci)
        random.shuffle(igraci)
        igraci = tuple(igraci)
    else:
        raise RuntimeError("Dodatni argument `{0:s}' nije prepoznat.".format(sys.argv[1]))
elif len(sys.argv) != 1:
    raise RuntimeError("Skripta se pokrece s jednim argumentom `-r' (obrnuti redoslijed igraca) ili `-p' (slucajni redoslijed igraca), ili bez argumenata.")

# Inicijalizacija igre.
igra = Tablic()

# Dodabvanje igraca u igru.
for igrac in igraci:
    igra.dodajIgraca(igrac['klasa'], *igrac['args'], **igrac['kwargs'])

# Igranje partije.
igra.igraj()
