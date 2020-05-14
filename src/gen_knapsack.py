# Generate from the configuration of knapsack game to payoff form .nfg format.

from itertools import product
import numpy as np
from game_utils import *


def gen_knapsack_nfg():
    for js in ls():
        print("Working on ", js.split('/')[-1])
        g = KnapsackGame(js)
        # Save the normal form game
        g.write_gamefile()


def gen_knapsack_json(m, n, suffix='3'):
    jsdata = \
        {
            "title": "Knapsack Game, normal form",
            "players": [str(p) for p in range(m)],
            "investments": [str(i) for i in range(n)],
            "w_pi": np.random.randint(1, 3, size=(m, n)).tolist(),
            "w_p": np.random.randint(1, n, size=m).tolist(),
            "v_pi": (2 * np.random.rand(m, n)).tolist(),
            "c_kpi": 1
        }
    dumpjs(jsdata, 'knapsack' + suffix)


def main():
    for (m, n) in [(6, 8)]:
        for i in range(10):
            gen_knapsack_json(m, n, suffix='-{}-{}_{}'.format(m, n, i))


if __name__ == '__main__':
    main()
