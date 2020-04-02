
import sys
import os
import json
from itertools import product
import numpy as np

TESTDIR = "tests/"

def ls(suffix='.json'):
    if len(sys.argv) > 1:
        jslist = [TESTDIR + f + suffix for f in sys.argv[1:]]
    else:
        jslist = [os.path.join(root, f) for root, _, files in os.walk(TESTDIR)
                  for f in files if f.endswith(suffix)]
        print("No knapsack json file listed. The test foler contains: \n \t ", jslist)
        y = input("Go over all of them? [y/n] > ")
        if y.lower() != 'y':
            print("Abort.")
            return
    for j in jslist:
        yield j

class KnapsackGame:
    def __init__(self, js):
        """
        save the json file into a class, compute strategies.
        """
        with open(js, 'r') as fjs:
            ks = json.load(fjs)
        self.title = ks['title']
        self.players = ks['players']
        self.n = len(ks['investments'])
        self.m = len(ks['players'])
        self.wpi = np.array(ks['w_pi'])
        self.wp = np.array(ks['w_p'])
        self.vpi = np.array(ks['v_pi'])
        self.ckpi = int(ks['c_kpi']) # for simplify assumes that ckpi is a constant.
        # Figure out the strategy based on budget constraints,
        # Each entry of the strategies correspond the options of a player.
        self.strategies = []
        for wi, w in zip(self.wpi, self.wp):
            lsi = []
            for si in product([0, 1], repeat=self.n):
                if wi.dot(si) <= w:
                    lsi.append(si)
            self.strategies.append(lsi)
        self.ns = [len(s) for s in self.strategies] # number of pure strategies
        # print(self.strategies)
