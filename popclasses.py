import numbers # To check if a type is numeric
import numpy as np
import time

from constants import model_constants # Import model constants

# Implement classes

# Takes a list of seven numbers as input and outputs a dictionary containing the corresponding genes.
class Genome(dict):
	def __init__(self,lst):
		super(Genome,self).__init__()
		if ((len(lst) == 7) & (all(isinstance(x,numbers.Number) for x in lst))):
			self['h'] = lst[0]
			self['s'] = lst[1]
			self['a'] = lst[2]
			self['I0'] = lst[3]
			self['I0p'] = lst[4]
			self['b'] = lst[5]
			self['bp'] = lst[6]
			self._constants = model_constants()
		else:
			raise TypeError('Argument must be a list of 7 numbers.')

	def mutate(self):
		mu = self._constants.mu

		for gene in ['h','s','I0','I0p']:
			r = np.random.rand()
			if (r<=mu):
				mutation_step = np.random.normal(loc=0,scale=0.05)
				self[gene] = self[gene] + mutation_step

		if (self['s'] > 0.5):
			for gene in ['a','b','bp']:
				r = np.random.rand()
				if (r<=mu):
					mutation_step = np.random.normal(loc=0,scale=0.05)
					self[gene] = self[gene] + mutation_step
		else:
			self['a'], self['b'], self['bp'] = 0, 0, 0

		return self



# Takes a Genome as input and outputs an Animal with traits genes, mismatch, adjustments and insulation.
class Animal:
	def __init__(self,*args):
		if (len(args) > 0):
			genes = args[0]
		else:
			genes = self._random_genes()

		if isinstance(genes,Genome):
			self.genes = genes
			self.mismatch = 0
			self.adjustments = 0
			self.insulation = genes['I0']
		else:
			raise TypeError('First argument must be of type Genome.')

	def _random_genes(self):
		rand_numbers = np.random.rand(6) # create 6 random genes in the interval [0,1)
		rand_genes = np.concatenate(([1],[1,1,2,2,4,4]*rand_numbers+[0,0,-1,-1,-2,-2]))
		genes = Genome(rand_genes)

		if (genes['s']<=0.5):
			genes['a'], genes['b'], genes['bp'] = 0, 0, 0
		return genes


# Takes a population size and a list of Animal as input and delivers a Population.
class Population:

	# Constructor of the population
	def __init__(self,size,animals):
		if (isinstance(size,int) & (all(isinstance(x,Animal) for x in animals))):
			if (size == len(animals)):
				self._animals = np.array(animals)
				self._size = size
				self._constants = model_constants()
			else:
				raise ValueError('The size parameter must be equal to the length of the list of animals.')
		else:
			raise TypeError('First argument must be of type int, second of type list of Animal.')

	# Outputs the ndarray of Animal 
	def animals(self):
		return self._animals

	# Changes a single Animal at list position i to Animal val
	def update(self,i,val):
		self._animals[i] = val

	# Outputs the current size of the population
	def size(self):
		return self._size

	# Calculates the insulation of each Animal in the Population based on cue C and environment E
	def react(self,E,C,*args):
		for (i,animal) in enumerate(self._animals):
			if (len(args) > 0):
				a = args[0]
			else:
				a = animal.genes['a']
			r = np.random.rand()
			if (r <= a):
				r = np.random.rand()
				if (r <= animal.genes['h']):
					new_insulation = animal.genes['I0']+animal.genes['b']*C
				else:
					new_insulation = animal.genes['I0p']+animal.genes['bp']*C
				self._animals[i].insulation = new_insulation
				self._animals[i].adjustments = self._animals[i].adjustments + 1

			self._animals[i].mismatch = self._animals[i].mismatch + np.abs(self._animals[i].insulation-E)


	# Calculates the lifetime payoff of a single Animal animal.
	def _lifetime_payoff(self,animal):
		tau = self._constants.tau
		if (animal.genes['s'] <= 0.5):
			return np.exp(-tau*animal.mismatch)
		else:	
			return max(np.exp(-tau*animal.mismatch) - self._constants.kd - animal.adjustments * self._constants.ka, 0)

	def _max_payoff(self,animal):
		if (animal.genes['s'] <= 0.5):
			return 1
		else:
			return max(1 - self._constants.kd - animal.adjustments * self._constants.ka, 0)

	# Iterates the entire Population to a new generation, calculating the number of offspring of each Animal.
	def breed_constant(self):
		lifetime_payoff = np.array(list(map(self._lifetime_payoff,self._animals)))
		mean_payoff = np.mean(lifetime_payoff)

		if (mean_payoff == 0):
			print(self._animals[0].mismatch)
			print(self._animals[0].insulation)
		else:
			payoff_factor = lifetime_payoff/mean_payoff

		new_animals = [self._breed(animal,payoff) for animal,payoff in zip(self._animals,payoff_factor)]
		new_animals = [item for sublist in new_animals for item in sublist]

		N = len(new_animals)
		print("Population size: {0}".format(N))
		if (N > self._constants.population_size):
			new_animals = np.random.choice(new_animals,self._constants.population_size,replace=False)
		elif (N < self._constants.population_size):
			new_animals = np.concatenate((new_animals,np.random.choice(new_animals,self._constants.population_size - N)))

		self._animals = new_animals


	def breed_variable(self):
		lifetime_payoff = np.zeros(self._size)
		max_payoff = np.zeros(self._size)
		for (i,animal) in enumerate(self._animals):
			lifetime_payoff[i] = self._lifetime_payoff(animal)
			max_payoff[i] = self._max_payoff(animal)

		new_animals = map(self._breed,self._animals,lifetime_payoff/max_payoff)
		new_animals = [item for sublist in new_animals for item in sublist]

		N = len(new_animals)
		if (N > self._constants.population_size):
			new_animals = np.random.choice(new_animals,self._constants.population_size)

		self._animals = new_animals
		self._size = len(new_animals)

	def _breed(self,animal,payoff_factor):
		offspring = np.random.poisson(lam=payoff_factor)
		new_animals = [Animal(animal.genes.mutate()) for _ in range(offspring)]
		return new_animals
