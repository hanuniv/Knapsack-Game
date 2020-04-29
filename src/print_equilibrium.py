
from game_utils import *

for gamefile in ls(suffix='.nfg'):
    mygame = KnapsackGame(gamefile.replace(".nfg", ".json"))
    for st_eq in mygame.enumerate_equilibrium():
        print(' & '.join([str(s) for s in st_eq]) + r'\\')
