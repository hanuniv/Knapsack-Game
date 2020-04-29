from gurobipy import *

import numpy as np

import game_utils

# import importlib
# importlib.reload(game_utils)

# Testing settings
# reldir = '../tests/'
# js = reldir + 'knapsack2.json'

def sample_gen(js, verify=False):
    g = game_utils.KnapsackGame(js)
    print("Working on ", js.split('/')[-1])
    if verify:
        all_eqn = g.all_eqns()
    substrategies = [[(0, 0, 0, 0)] for i in g.player_iter]
    while True:
        # find a nash equilibria
        g.set_strategies(substrategies)
        g.write_gamefile()
        eqns = list(g.enumerate_equilibrium())
        x = eqns[0]  # given one equilibrium
        payoffs = g.payoffs(np.array(x))
        improved=False
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
                substrategies[p].append(x[p])
                print("## Find a better alternative for p={} :".format(p), x)
                x[p] = oldxp
                print("# --- over ---> ", substrategies)
                improved = True
                # break # optionally early break
        if not improved:
            print("# Find Nash Equilibria", x)
            print("# --- over ---> ", substrategies)
            if verify and not (x in all_eqn):
                print("# ?????? WTF WTF ????? Something is not Nash????")
            break

def main():
    for js in game_utils.ls():
        sample_gen(js)

if __name__ == '__main__':
    main()
