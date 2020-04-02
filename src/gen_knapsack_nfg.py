# Generate from the configuration of knapsack game to payoff form .nfg format.

from itertools import product
import numpy as np
from  game_utils import *

def main():
    for js in ls():
        print("Working on ", js.split('/')[-1])
        g = KnapsackGame(js)
        # Save the normal form game
        nfg = js.replace(".json", ".nfg")
        with open(nfg, 'w') as fout:
            fout.write(
                "NFG 1 R \"" + g.title + '\" { \"' + "\" \"".join(g.players) + '\" } { ' +
                ' '.join([str(len(s)) for s in g.strategies]) + ' }\n\n')
            for s in product(*reversed(g.strategies)):  # iterate over the strategies in the order of the game
                xpi = np.array(list(reversed(s)))
                interact = g.ckpi * xpi.dot(xpi.T)
                np.fill_diagonal(interact, 0)
                payoff = np.sum(xpi * g.vpi, axis=1) + np.sum(interact, axis=1)
                # print(payoff)
                fout.write(' '.join(np.asarray(payoff, dtype=np.str)) + ' ')

if __name__ == '__main__':
    main()
