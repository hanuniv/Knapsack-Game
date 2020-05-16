Computing a Nash Equilibrium for Knapsack Games
=======

# Dependencies
Install GAMBIT by following the instructions from 
- http://www.gambit-project.org/gambit15/build.html#building-from-git-repository
- http://www.gambit-project.org/gambit15/build.html#building-the-python-extension

For the description of nfg file format, consult 
- http://www.gambit-project.org/gambit15/formats.html#the-strategic-game-nfg-file-format-payoff-version 

The sample generation algorithm depends on Gurobi
- https://www.gurobi.com/documentation/9.0/quickstart_linux/py_python_interface.html#section:Python 

# Contents  
- *src/gen_knapsack.py*: randomly generate the json configuration file for specific number of players and projects
- *src/game_utils.py*: Knapsack class, utilities for statistics reporting
- *src/sample_gen.py*: sample generation algorithm for solving knapsack games
- *tests/*: data for testing 

# Usage 
- Compute One Equilibrium for Knapsack Games 
`python src/sample_gen.py knapsack1 knapsack2`

- Compute all sample data file and obtain statistics 
`python src/sample_gen.py --all`
