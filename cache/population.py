import numbers # To check if a type is numeric
import numpy as np
import time
from copy import deepcopy
from constants import model_constants # Import model constants

from genome import Genome
from animal import Animal

# Implement Population class

# Takes a population size and a list of Animal as input and delivers a Population.
class Population:
	# Constructor of the population
	def __init__(self,size,animals):
		if (isinstance(size,int) & (all(isinstance(x,Animal) for x in animals))):
			if (size == len(animals)):
				self._animals 	= np.array(animals)
				self._size 		= size
				self._constants	= model_constants()
				self._positions = self.positions()
			else:
				raise ValueError('The size parameter must be equal to the length of the list of animals.')
		else:
			raise TypeError('First argument must be of type int, second of type list of Animal.')

	# Outputs the ndarray of animals 
	def animals(self):
		return self._animals

	# Outputs the current size of the population
	def size(self):
		return self._size

	# Calculates the insulation of each Animal in the Population based on cue C and environment E
	def react(self,E,C,evolve_all=False):
		for animal in self._animals:
			animal.react(E,C,evolve_all)

	# Iterates the entire Population to a new generation, calculating the number of offspring of each Animal.
	def breed_constant(self):
		calc_payoff 	= np.vectorize(lambda x: x.lifetime_payoff(self._positions))
		lifetime_payoff = calc_payoff(self._animals)
		mean_payoff 	= np.mean(lifetime_payoff)
		print(self._positions)
		if (mean_payoff == 0):
			raise RuntimeError("Mean payoff of population decreased to 0. Check your parameters!")
		else:
			payoff_factor = lifetime_payoff/mean_payoff

		offspring 		= np.random.poisson(lam=payoff_factor)
		born_animals 	= np.repeat(self._animals,offspring)
		mutate_pop 		= np.vectorize(lambda x: Animal(x.genes.mutate(),x.position))
		new_animals 	= mutate_pop(born_animals)

		N = len(new_animals)
		print("Population size: {0}\tMean payoff: {1:.2f}".format(N,mean_payoff))
		if (N > self._constants["population_size"]):
			new_animals = np.random.choice(new_animals,self._constants["population_size"],replace=False)
		elif (N < self._constants["population_size"]):
			copy_clones = np.vectorize(deepcopy)
			clones 		= copy_clones(np.random.choice(new_animals,self._constants["population_size"] - N))
			new_animals = np.append(new_animals,clones)

		self._animals 	= new_animals
		self._positions = self.positions()


	def breed_variable(self): 
		calc_payoff 	= np.vectorize(lambda x: x.lifetime_payoff(self._positions))
		lifetime_payoff = calc_payoff(self._animals)
		max_payoff 		= 1.0/self._constants["q"]
		payoff_factor 	= lifetime_payoff/max_payoff
		offspring 		= np.random.poisson(lam=payoff_factor)
		born_animals 	= np.repeat(self._animals,offspring)

		try:
			born_animals[0]
		except IndexError:
			self._size = 0
			return

		mutate_pop 		= np.vectorize(lambda x: Animal(x.genes.mutate(),x.position))
		new_animals 	= mutate_pop(born_animals)

		N = len(new_animals)
		print("Population size: {0}".format(N))
		if (N > self._constants["population_size"]):
			new_animals = np.random.choice(new_animals,self._constants["population_size"],replace=False)

		self._animals 	= new_animals
		self._size 		= len(new_animals)
		self._positions	= self.positions()

	def positions(self):
		fun = np.vectorize(lambda x: x.position)
		pos = fun(self._animals)
		return np.bincount(pos,minlength=len(self._constants["environments"]))