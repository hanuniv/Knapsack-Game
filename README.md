Code for Computing Nash Equilibrium 
=======

# Setting up the gambit environment
Follow instructions from the 
- http://www.gambit-project.org/gambit15/build.html#building-from-git-repository
- http://www.gambit-project.org/gambit15/build.html#building-the-python-extension

# Contents  
- *src/generate_knapsack.py*: generate the form of the game for the 
- *tests/*: data for testing 

# Obtain Pure Equilibrium for Knapsack Problems 
- edit the files in tests/, e.g. `knapsack1.json`
- generate normal form game files `python src/gen_kanpsack_nfg.py [knapsack1]`. See http://www.gambit-project.org/gambit15/formats.html#the-strategic-game-nfg-file-format-payoff-version for the description of nfg file format. 
- save the equilibrium and print equilibirum in latex ```python src/print_equilibirum.py [kanpsack1]````

# Compute One Equilibrium for Knapsack Games 
    `python src/sample_gen.py knapsack1 knapsack2`
