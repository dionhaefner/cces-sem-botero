#########################################################
#	genome.py
#	Author: Dion Häfner (dionhaefner@web.de)
#	
#	Implementing Genome class and methods
#	
#	Licensed under BSD 2-Clause License
#########################################################


import numbers
import numpy as np

from constants import model_constants


class Genome(dict):
	def __init__(self,lst):
	# Takes a list of seven numbers as input and outputs a dictionary containing the corresponding genes.
		super(Genome,self).__init__()
		if ((len(lst) == 9) & (all(isinstance(x,numbers.Number) for x in lst))):
			self['h'] 		= lst[0]
			self['s'] 		= lst[1]
			self['a'] 		= lst[2]
			self['I0'] 		= lst[3]
			self['I0p']		= lst[4]
			self['b'] 		= lst[5]
			self['bp'] 		= lst[6]
			self['m']		= lst[7]
			self['ma']		= lst[8]
			self._constants = model_constants()
		else:
			raise TypeError('Argument must be a list of 9 numbers.')

	def mutate(self):
	# Mutates the genome
		mu = self._constants["mu"]
		for gene in ['h','s','I0','I0p','m']:
			r = np.random.rand()
			if (r<=mu):
				mutation_step = np.random.normal(loc=0,scale=0.05)
				self[gene] = self[gene] + mutation_step

		if (self['s'] > 0.5):
			for gene in ['a','b','bp','ma']:
				r = np.random.rand()
				if (r<=mu):
					mutation_step = np.random.normal(loc=0,scale=0.05)
					self[gene] = self[gene] + mutation_step
		else:
			self['a'], self['b'], self['bp'] = 0, 0, 0

		for gene in self._constants["limit"]:
			self[gene] = min(1,max(0,self[gene]))
				
		return self