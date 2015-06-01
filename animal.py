import numpy as np
from constants import model_constants # Import model constants
from genome import Genome

# Implement Animal class

# Takes a Genome as input and outputs an Animal with traits genes, mismatch, adjustments and insulation.
class Animal:
	def __init__(self,*args):
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
			

	def _random_genes(self):
		rand_numbers = np.random.rand(8) # create 8 random genes in the interval [0,1)
		rand_genes = np.concatenate(([1],[1,1,2,2,4,4,0,0]*rand_numbers+[0,0,-1,-1,-2,-2,0,0]))
		genes = Genome(rand_genes)

		if (genes['s']<=0.5):
			genes['a'], genes['b'], genes['bp'], genes['ma'] = 0, 0, 0, 0
		return genes

	def react(self,E,C,evolve_all=False):
		pos = self.position
		r = np.random.rand()
		if ((r <= self.genes['ma']) | evolve_all):
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
		tau 			= self._constants["tau"]
		scale_factor 	= 1 - positions[self.position] / self._constants["population_size"]
		if (self.genes['s'] <= 0.5):
			return scale_factor * max(np.exp(-tau*self.mismatch) - self._constants["km"] * self.migrations, 0)
		else:	
			return scale_factor * max(np.exp(-tau*self.mismatch) - self._constants["kd"] - self.adjustments * self._constants["ka"] - self._constants["km"] * self.migrations, 0)

	def _scale(self,x):
		if x < 0:
			return -1*np.log(np.abs(x)+1)/np.log(3)
		else:
			return np.log(np.abs(x)+1)/np.log(3)