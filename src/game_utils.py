
import sys
import os
import json
from itertools import product
import numpy as np
import gambit

TESTDIR = "tests/"


def ls(lst=None, prefix='', suffix='.json', substr='', exclude='_stat'):
    """
    list file names with given suffix without arguments, if arguments are given, loop over given files (without suffix)

    call ls(), loop over all test files or file given by the command line
    call ls(prefix='knapsack1') loop over test files with prefix 'knapsack1'
    """
    if lst is not None and prefix == '' and substr == '':
        jslist = [TESTDIR + f + suffix for f in lst]
    else:
        jslist = [os.path.join(root, f) for root, _, files in os.walk(TESTDIR)
                  for f in files if f.endswith(suffix) and f.startswith(prefix) and substr in f and exclude not in f]
        print("No knapsack json file listed. The test foler contains: \n \t ", jslist)
        y = input("Go over all of them? [y/n] > ")
        if y.lower() != 'y':
            print("Abort.")
            return
    for j in jslist:
        yield j


def dumpjs(js, filename):
    with open(TESTDIR + filename + '.json', 'w') as lf:
        json.dump(js, lf, indent=4)


def stat(filename):
    """
    return the mean and standard deviation of the statistic file

    e.g. stat('knapsack-3-4')
    """
    with open(TESTDIR + filename + '_stat.json', 'r') as fjs:
        data = json.load(fjs)
    data = np.array(data)
    return np.mean(data, axis=0), np.std(data, axis=0)


class KnapsackGame:
    def __init__(self, js, gen_strategies=False):
        """
        save the json file into a class, compute strategies.
        """
        with open(js, 'r') as fjs:
            ks = json.load(fjs)
        self.js = js
        self.nfg = js.replace(".json", ".nfg")  # default nfg file name, may not exist
        self._nfg = js.replace(".json", "_.nfg")  # default data file
        self.title = ks['title']
        self.players = ks['players']
        self.n = len(ks['investments'])
        self.m = len(ks['players'])
        self.player_iter = range(self.m)
        self.invest_iter = range(self.n)
        self.wpi = np.array(ks['w_pi'])
        self.wp = np.array(ks['w_p'])
        self.vpi = np.array(ks['v_pi'])
        self.ckpi = int(ks['c_kpi'])  # for simplify assumes that ckpi is a constant.
        if gen_strategies:
            self._gen_strategies()

    def payoffs(self, xpi):
        """
        returns the payoff of strategy xpi

        xpi is an np.ndarray whose (p,i) entry is the choice of player p for item i
        """
        interact = self.ckpi * xpi.dot(xpi.T)
        np.fill_diagonal(interact, 0)
        payoff = np.sum(xpi * self.vpi, axis=1) + np.sum(interact, axis=1)
        return payoff

    def all_eqns(self):
        if not hasattr(self, "_all_eqns"):  # cache the results
            self._gen_strategies()
            self.write_gamefile(use_=True)
            self._all_eqns = list(self.enumerate_equilibrium(use_=True))
        return self._all_eqns

    def current_eqns(self):
        return list(self.enumerate_equilibrium(use_=False))

    def _gen_strategies(self):
        # Figure out the strategy based on budget constraints,
        # Each entry of the strategies correspond the options of a player.
        if hasattr(self, '_strategies'):   # cache it for repeated tests
            self.strategies = self._strategies
        else:
            self.strategies = []
            for wi, w in zip(self.wpi, self.wp):
                lsi = []
                for si in product([0, 1], repeat=self.n):
                    if wi.dot(si) <= w:
                        lsi.append(si)
                self.strategies.append(lsi)
            self.ns = [len(s) for s in self.strategies]  # number of pure strategies
            self._strategies = self.strategies
        # print(self.strategies)

    def set_strategies(self, strategies):
        self.strategies = strategies
        self.ns = [len(s) for s in self.strategies]

    def write_gamefile(self, use_=False):
        """
        Save the gamefile given current set of strategies, the default is *.json -> *.nfg

        when use_=True , use *_.nfg,  the file is only created once.
        """
        if use_:
            nfg = self._nfg
            if os.path.exists(self._nfg):
                return
        else:
            nfg = self.nfg
        if not hasattr(self, "strategies"):
            self._gen_strategies()
        with open(nfg, 'w') as fout:
            fout.write(
                "NFG 1 R \"" + self.title + '\" { \"' + "\" \"".join(self.players) + '\" } { ' +
                ' '.join([str(len(s)) for s in self.strategies]) + ' }\n\n')
            for s in product(*reversed(self.strategies)):  # iterate over the strategies in the order of the game
                xpi = np.array(list(reversed(s)))
                payoff = self.payoffs(xpi)
                # print(payoff)
                fout.write(' '.join(np.asarray(payoff, dtype=np.str)) + ' ')

    def enumerate_equilibrium(self, use_=False):
        """
        Find the equilibrium of the game with gambit
        """
        if use_:
            nfg = self._nfg
        else:
            nfg = self.nfg
        gambitg = gambit.Game.read_game(nfg)
        # solver = gambit.nash.ExternalEnumPureSolver()
        # nash_eqs = solver.solve(g)
        nash_eqs = gambit.nash.enumpure_solve(gambitg)
        for eq in nash_eqs:
            # print(np.nonzero(eq)[0])
            # print(np.asarray(eq, dtype=np.int))
            # obtain index of the best strategies.
            index_eq = (np.nonzero(eq)[0] - np.cumsum([0] + self.ns[:-1]))
            st_eq = [st[i] for i, st in zip(index_eq, self.strategies)]
            yield st_eq
