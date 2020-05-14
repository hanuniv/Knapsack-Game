from gurobipy import *

import numpy as np

import game_utils

from datetime import datetime

import argparse

# import importlib
# importlib.reload(game_utils)

# Testing settings
# TESTDIR = '../tests/'
# js = reldir + 'knapsack2.json'


def sample_gen(g):
    """
    samle generation algorithm for finding nash equilibria
    """
    substrategies = [[tuple([0] * (g.n))] for i in g.player_iter]
    while True:
        # find a nash equilibria
        g.set_strategies(substrategies)
        g.write_gamefile()
        eqns = g.current_eqns()
        x = eqns[0]  # given one equilibrium
        payoffs = g.payoffs(np.array(x))
        improved = False
        for p in g.player_iter:  # for each player
            m = Model("sample_gen")
            y = m.addVars(g.invest_iter, vtype=GRB.BINARY, name="alternative")
            m.modelSense = GRB.MAXIMIZE
            # m.setObjective(quicksum(y[i] for i in g.invest_iter))
            m.setObjective(quicksum(y[i] * g.vpi[p, i] for i in g.invest_iter)
                           + quicksum(g.ckpi * y[i] * x[q][i] for i in g.invest_iter for q in g.player_iter if q != p))
            wi = g.wpi[p]
            w = g.wp[p]
            m.addConstr(quicksum(wi[i] * y[i] for i in g.invest_iter) <= w, "capacity")
            m.update()
            m.optimize()
            if m.objVal > payoffs[p]:
                oldxp = x[p]
                x[p] = tuple(int(y[i].x) for i in g.invest_iter)
                if x[p] not in substrategies[p]:
                    substrategies[p].append(x[p])
                    print("## Find a better alternative for p={} :".format(p), x)
                    print("# --- over ---> ", substrategies)
                    improved = True
                    break  # optionally early break
                x[p] = oldxp
        if not improved:
            print("# Find Nash Equilibria", x)
            print("# --- over ---> ", substrategies)
            break
    return x


def compare_sample_gen(js, verify=False, use_gambit=False):
    """
    compare sample generation algorithm with gambit
    """
    g = game_utils.KnapsackGame(js)
    print("Working on ", js.split('/')[-1])
    # all_eqn_start= datetime.now()
    form_start = datetime.now()
    if use_gambit:
        g._gen_strategies()
        g.write_gamefile()
    form_end = datetime.now()
    compute_start = datetime.now()
    if use_gambit:
        all_eqn = g.current_eqns()
    compute_end = datetime.now()
    # all_eqn_end = datetime.now()
    sample_gen_start = datetime.now()
    x = sample_gen(g)
    sample_gen_end = datetime.now()
    if verify and not (x in all_eqn):
        print("# ?????? WTF WTF ????? Something is not Nash????")
    return ((form_end - form_start).total_seconds(), (compute_end - compute_start).total_seconds(), (sample_gen_end - sample_gen_start).total_seconds())


def alltests():
    # msns = [(3, 4), (6, 4), (3, 8), (6, 8)]
    msns = [(3, 8)]
    for m, n in msns:
        substr = "-{}-{}".format(m, n)
        try:
            alltime = []
            for js in game_utils.ls(prefix='knapsack' + substr):
                stopwatch = compare_sample_gen(js, verify=True)
                alltime.append(stopwatch)
        finally:
            game_utils.dumpjs(alltime, 'knapsack' + substr + '_stat')
            timestat = game_utils.stat('knapsack' + substr)
            print(">>>>>>>> Statistics of the execution", timestat)


def main():
    parser = argparse.ArgumentParser(
        description='Run Sample Generation Algorithm')
    parser.add_argument(dest='filenames', metavar='filename',
                        nargs='*')  # may add tags to filenames

    parser.add_argument('-a', '--all', dest='all', action='store_true',
                        help='Run all tests')

    args = parser.parse_args()

    if args.all:
        alltests()
    elif args.filenames:
        print(args.filenames)
        for js in game_utils.ls(lst=args.filenames):
            timestat = compare_sample_gen(js, verify=True)
            print(timestat)


if __name__ == '__main__':
    main()
