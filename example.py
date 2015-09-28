#!/usr/bin/env python
# -*- coding: utf8 -*-

#########################################################
#
#	example.py
#	Author: Dion Häfner (dionhaefner@web.de)
#	
#	Demonstrates the usage of custom classes
#
#	Licensed under BSD 2-Clause License
#
#########################################################

import sys
sys.path.insert(0, './src')

#
# Import third-party packages
#

import numpy as np # For efficient array operations
import matplotlib.pyplot as plt # For plotting

try: # Seaborn makes prettier plots, but is not installed in a fresh Anaconda python
	import seaborn as sns 
	have_seaborn = True
except ImportError:
	have_seaborn = False

#
# Import other parts of the project
#

from animal import Animal
from population import Population
from environment import Environment
from constants import model_constants
from iterate_population import iterate_population


#
# Example usage of classes
#

# Create an Animal and operate on it
genes = np.array([1.512,2,3,4,5,6,7,8,9])
duck = Animal(genes,0)

print(duck.genes)
print(duck.genes['I0'])
print(duck.mismatch)

# To create an Animal with randomly drawn genes, just omit the argument:
random_duck = Animal()
print(random_duck.gene_dict)
print(random_duck.genes)

# These raise an error:
# wrong_duck = Animal([1,2,3,4,5,6,7,8,9]) - argument must be a 'Genome'
# wrong_genes = Genome([1,2,3,4,5,6]) - argument is too short

# Mutate an Animal's genes
print(random_duck.mutate())


# Create an Environment
R, P, A, B, O = 10, 0.5, 1, 0.5, 0
test_env = Environment(R,P,A,B,O,name="Test environment")

# Evaluate the state of the environment at a given time
t = 10
E,C = test_env.evaluate(t)

# E and C must be of type list of float to allow for multiple environments
# Consider three equal environments:
E,C = [E,E,E], [C,C,C]

# Let the animals react to the environment
random_duck.react(E,C)

# Access some information about the animal
print(random_duck.mismatch)
print(random_duck.lifetime_payoff([1000]))

# Create some more animals and combine them to a Population
more_ducks = [Animal(),Animal(),Animal()]
duck_population = Population(len(more_ducks),more_ducks)

# Make them react to the environment and breed with variable population size
duck_population.react(E,C)
duck_population.breed_variable()

# Display the new size of the population
print(duck_population.size())
