Code for Computing Nash Equilibrium 
=======

# Setting up the gambit environment
Follow instructions from the 
- http://www.gambit-project.org/gambit15/build.html#building-from-git-repository
- http://www.gambit-project.org/gambit15/build.html#building-the-python-extension

See http://www.gambit-project.org/gambit15/formats.html#the-strategic-game-nfg-file-format-payoff-version for the description of nfg file format. 

# Contents  
- *src/generate_knapsack.py*: generate the form of the game for the 
- *tests/*: data for testing 

# Obtain All pure Equilibrium for Knapsack Problems 
- save the equilibrium and print equilibirum in latex 
    `python src/print_equilibirum.py [kanpsack1]`

# Compute One Equilibrium for Knapsack Games 
`python src/sample_gen.py knapsack1 knapsack2`

# Compute all sample data file and obtain statistics 
`python src/sample_gen.py --all`
