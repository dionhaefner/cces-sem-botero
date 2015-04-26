import numpy as np # For efficient array operations
import matplotlib.pyplot as plt # For plotting
import seaborn as sns # Makes prettier plots
from popclasses import * # Import custom classes
from constants import model_constants # Import model constants
from environment import * # Import environment model

# Sets the style of the plots
sns.set(style='ticks', palette='Set2')

# Example usage of classes
genes = Genome([1.512,2,3,4,5,6,7])
duck = Animal(genes)

print(duck.genes)
print(duck.genes['I0'])
print(duck.mismatch)

# To create an Animal with randomly drawn genes, just omit the argument:
random_duck = Animal()
print(random_duck.genes) 

# These raise an error:
# wrong_duck = Animal([1,2,3,4,5,6,7]) - argument must be a 'Genome'
# wrong_genes = Genome([1,2,3,4,5,6]) - argument is too short

print(random_duck.genes.mutate())