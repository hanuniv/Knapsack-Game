# Generate from the configuration of knapsack game to payoff form .nfg format.

from itertools import product
import numpy as np
from  game_utils import *

def main():
    for js in ls():
        print("Working on ", js.split('/')[-1])
        g = KnapsackGame(js)
        # Save the normal form game
        g.write_gamefile()

if __name__ == '__main__':
    main()
