#########################################################
#	animal.py
#	Author: Dion Häfner (dionhaefner@web.de)
#	
#	Implementing Animal class and methods
#	
#	Licensed under BSD 2-Clause License
#########################################################


import numpy as np

from constants import model_constants
from genome import Genome


class Animal:
	def __init__(self,*args):
	# Takes a Genome as input and outputs an Animal with traits genes,
	# mismatch, adjustments and insulation.
		self._constants = model_constants()
		if (len(args) > 0):
			genes 		= args[0]
			position 	= args[1]
			if not isinstance(genes,Genome):
				raise TypeError('First argument must be of type Genome.')
		else:
			genes 		= self._random_genes()
			position 	= np.random.randint(len(self._constants["environments"]))

		self.genes 			= genes
		self.mismatch 		= 0
		self.adjustments	= 0
		self.migrations		= 0
		self.insulation 	= genes['I0']
		self.position		= position

# PUBLIC METHODS			

	def react(self,E,C,evolve_all=False):
	# Animal migrates and reacts to environment E and cue C. If evolve_all is set, reaction takes place
	# for all animals, regardless of gene 'a'.
		pos = self.position
		r = np.random.rand()
		if (((r <= self.genes['ma']) | evolve_all) & (len(self._constants["environments"]) > 1)):
			r = np.random.rand()
			if (r <= self.genes['m']):
				positions 			= np.arange(len(self._constants["environments"]))
				new_position 		= np.random.choice(positions[positions!=pos])
				self.position 		= new_position
				self.migrations 	+= 1

		r = np.random.rand()
		if ((r <= self.genes['a']) | evolve_all):
			r = np.random.rand()
			if (r <= self.genes['h']):
				new_insulation = self._scale(self.genes['I0'])+self._scale(self.genes['b'])*C[pos]
			else:
				new_insulation = self._scale(self.genes['I0p'])+self._scale(self.genes['bp'])*C[pos]

			self.insulation 	= new_insulation
			self.adjustments 	= self.adjustments + 1

		self.mismatch = self.mismatch + np.abs(self.insulation-E[pos])


	def lifetime_payoff(self,positions):
	# Assembles the lifetime payoff of the animal
		tau 			= self._constants["tau"]
		if len(positions) > 1:
			scale_factor = 1 - positions[self.position] / self._constants["population_size"]
		else:
			scale_factor = 1
		if (self.genes['s'] <= 0.5):
			return scale_factor * max(np.exp(-tau*self.mismatch) - self._constants["km"] * self.migrations, 0)
		else:	
			return scale_factor * max(np.exp(-tau*self.mismatch) - self._constants["kd"] \
				- self.adjustments * self._constants["ka"] - self._constants["km"] * self.migrations, 0)

# PROTECTED METHODS

	def _random_genes(self):
	# Returns random values for the 9 genes in the chosen intervals:
	# h: 1, s: [0,1], a: [0,1], I0: [-1,1], I0p: [-1,1], b: [-2,2], bp: [-2,2], m: 0, ma: 0
		rand_numbers = np.random.rand(9)
		rand_genes = [0,1,1,2,2,4,4,0,0]*rand_numbers+[1,0,0,-1,-1,-2,-2,0,0]
		genes = Genome(rand_genes)

		if (genes['s']<=0.5):
			genes['a'], genes['b'], genes['bp'], genes['ma'] = 0, 0, 0, 0
		return genes

	def _scale(self,x):
	# Defines the scale function, decreasing gene efficiency for extreme values
		if x < 0:
			return -1*np.log(np.abs(x)+1)/np.log(3)
		else:
			return np.log(np.abs(x)+1)/np.log(3)