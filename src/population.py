#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
#########################################################
#
#	population.py
#	Author: Dion Häfner (dionhaefner@web.de)
#	
#	Implements Population class
#	
#	Licensed under BSD 2-Clause License
#
#########################################################
"""

import numbers
import numpy as np
import time

from constants import model_constants # Import model constants
from animal import Animal


class Population:
	def __init__(self,size,animals):
		"""Takes a population size and a list of Animal as input"""
		if (isinstance(size,int) & (all(isinstance(x,Animal) for x in animals))):
			if (size == len(animals)):
				self._animals 	= np.array(animals)
				self._size = size
				self._constants	= model_constants
				self._positions = self.positions()
			else:
				raise ValueError('The size parameter must be equal to the length of the list of animals.')
		else:
			raise TypeError('First argument must be of type int, second of type list of Animal.')

	def animals(self):
		"""Returns the ndarray of animals"""
		return self._animals

	def size(self):
		"""Returns the current size of the population"""
		return self._size

	def react(self,E,C,evolve_all=False):
		"""Calculates the insulation of each Animal in the Population based on cue C and environment E"""
		for animal in self._animals:
			animal.react(E,C,evolve_all)

	def breed_constant(self):
		"""Iterates the entire Population to a new generation, calculating the number of offspring of each Animal with CONSTANT population size"""
		calc_payoff 	= np.vectorize(lambda x: x.lifetime_payoff(self._positions))
		lifetime_payoff = calc_payoff(self._animals)
		mean_payoff 	= np.mean(lifetime_payoff)

		if (mean_payoff == 0):
			raise RuntimeError("Mean payoff of population decreased to 0. Check your parameters!")
		else:
			payoff_factor = lifetime_payoff/mean_payoff

		offspring = np.random.poisson(lam=payoff_factor)
		born_animals = np.repeat(self._animals,offspring)
		mutate_pop = np.vectorize(lambda x: Animal(x.mutate(),x.position))
		new_animals = mutate_pop(born_animals)

		N = len(new_animals)
		if self._constants["verbose"]:
			print("\n\nAnimals per environment: {0}".format(self._positions))
			print("Population size: {0}\tMean payoff: {1:.2f}".format(N,mean_payoff))
		if (N > self._constants["population_size"]):
			new_animals = np.random.choice(new_animals,self._constants["population_size"]\
							,replace=False)
		elif (N < self._constants["population_size"]):
			clone_candidates = np.random.choice(new_animals,\
						self._constants["population_size"] - N)
			clones = [Animal(x.genes,x.position) for x in clone_candidates]
			new_animals = np.append(new_animals,clones)

		self._animals 	= new_animals
		self._positions = self.positions()


	def breed_variable(self):
		"""Iterates the entire Population to a new generation, calculating the number of offspring of each Animal with VARIABLE population size"""
		nE = len(self._constants["environments"])
		calc_payoff 	= np.vectorize(lambda x: x.lifetime_payoff(self._positions))
		lifetime_payoff = calc_payoff(self._animals)
		max_payoff 	= 1/self._constants["q"] #(1-1/nE)/self._constants["q"]
		payoff_factor 	= lifetime_payoff/max_payoff
		offspring 	= np.random.poisson(lam=payoff_factor)
		born_animals 	= np.repeat(self._animals,offspring)

		try: # check if all animals are dead yet
			born_animals[0]
		except IndexError:
			self._size = 0
			return

		mutate_pop = np.vectorize(lambda x: Animal(x.mutate(),x.position))
		new_animals = mutate_pop(born_animals)

		N = len(new_animals)
		if self._constants["verbose"]:
			print("\n\nAnimals per environment: {0}".format(self._positions))
			print("Population size: {0}".format(N))
		if (N > self._constants["population_size"]):
			new_animals = np.random.choice(new_animals,self._constants["population_size"]\
							,replace=False)

		self._animals = new_animals
		self._size = len(new_animals)
		self._positions	= self.positions()

	def positions(self):
		"""Returns the number of animals in each environment"""
		fun = np.vectorize(lambda x: x.position)
		pos = fun(self._animals)
		return np.bincount(pos,minlength=len(self._constants["environments"]))
