import gambit
from game_utils import *
import numpy as np

for gamefile in ls(suffix='.nfg'):
    mygame = KnapsackGame(gamefile.replace(".nfg", ".json"))
    g = gambit.Game.read_game(gamefile)
    # solver = gambit.nash.ExternalEnumPureSolver()
    # nash_eqs = solver.solve(g)
    nash_eqs = gambit.nash.enumpure_solve(g)
    for eq in nash_eqs:
        # print(np.nonzero(eq)[0])
        # print(np.asarray(eq, dtype=np.int))
        # obtain index of the best strategies.
        index_eq = (np.nonzero(eq)[0] - np.cumsum([0] + mygame.ns[:-1]))
        st_eq = [st[i] for i, st in zip(index_eq, mygame.strategies)]
        print(' & '.join([str(s) for s in st_eq]) + r'\\')
