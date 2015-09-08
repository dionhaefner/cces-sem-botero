#########################################################
#	animal.pyx
#	Author: Dion Häfner (dionhaefner@web.de)
#	
#	Implementing Animal class and methods
#	(cythonized version of animal.py and genome.py)
#
#	Licensed under BSD 2-Clause License
#########################################################


import numpy as np

cimport numpy as np
from libc.math cimport abs as c_abs
from libc.math cimport log as c_log
from libc.math cimport exp as c_exp
from libc.stdlib cimport rand as c_rand
from libc.stdlib cimport RAND_MAX

DTYPE = np.int
BTYPE = np.uint8
ctypedef np.int_t DTYPE_t
ctypedef np.uint8_t BTYPE_t

from constants import model_constants

cdef int nE = len(model_constants["environments"])

cdef class Animal:
	cdef object _constants
	cdef double h,s,a,I0,I0p,b,bp,m,ma
	cdef double mismatch
	cdef int adjustments
	cdef int migrations
	cdef double insulation
	cdef public int position


	def __init__(self,np.ndarray[double,ndim=1] genes=np.array([]),int position=nE+1):
	# Takes a Genome as input and outputs an Animal with traits genes,
	# mismatch, adjustments and insulation.
		if not genes.size:
			genes = random_genes()

		if position > nE:
			position = np.random.randint(nE)

		self.genes = genes
		self._constants = model_constants
		self.mismatch = 0
		self.adjustments = 0
		self.migrations	= 0
		self.insulation = genes[3]
		self.position = position
		

# PUBLIC METHODS			

	cpdef react(self,np.ndarray[double,ndim=1] E,np.ndarray[double,ndim=1] C,BTYPE_t evolve_all=0):
	# Animal migrates and reacts to environment E and cue C. If evolve_all is set, reaction takes place
	# for all animals, regardless of gene 'a'.
		cdef np.ndarray[DTYPE_t,ndim=1] positions
		cdef int new_position
		cdef float new_insulation
		cdef float r

		r = randnum()
		if (((r <= self.ma) | evolve_all) & (nE > 1)):
			r = randnum()
			if (r <= self.m):
				positions = np.arange(nE)
				new_position = np.random.choice(positions[positions!=self.position])
				self.position = new_position
				self.migrations += 1

		r = randnum()
		if ((r <= self.a) | evolve_all):
			r = randnum()
			if (r <= self.h):
				new_insulation = scale(self.I0)+scale(self.b)*C[self.position]
			else:
				new_insulation = scale(self.I0p)+scale(self.bp)*C[self.position]

			self.insulation = new_insulation
		self.mismatch = self.mismatch + c_abs(self.insulation-E[self.position])


	cpdef lifetime_payoff(self,np.ndarray[DTYPE_t] positions):
	# Assembles the lifetime payoff of the animal
		cdef double scale_factor
		cdef double tau = self._constants["tau"]
		if len(positions) > 1:
			scale_factor = 1 - positions[self.position] / self._constants["population_size"]
		else:
			scale_factor = 1
		if (self.s <= 0.5):
			return scale_factor * max(c_exp(-tau*self.mismatch) - self._constants["km"] * self.migrations, 0)
		else:	
			return scale_factor * max(c_exp(-tau*self.mismatch) - self._constants["kd"] \
				- self.adjustments * self._constants["ka"] - self._constants["km"] * self.migrations, 0)


	property gene_dict:
		def __get__(self):
			return {"h":self.h,"s":self.s,"a":self.a,"I0":self.I0,"I0p":self.I0p,"b":self.b,"bp":self.bp,"m":self.m,"ma":self.ma}

		def __set__(self,object genes):
			self.h = genes["h"]
			self.s = genes["s"]
			self.a = genes["a"]
			self.I0 = genes["I0"]
			self.I0p = genes["I0p"]
			self.b = genes["b"]
			self.bp = genes["bp"]
			self.m = genes["m"]
			self.ma = genes["ma"]
				
	property genes:
		def __get__(self):
			return np.array([self.h,self.s,self.a,self.I0,self.I0p,self.b,self.bp,self.m,self.ma])

		def __set__(self, object genes):
			self.h 	= genes[0]
			self.s 	= genes[1]
			self.a 	= genes[2]
			self.I0 = genes[3]
			self.I0p = genes[4]
			self.b 	= genes[5]
			self.bp = genes[6]
			self.m	= genes[7]
			self.ma	= genes[8]
		
	cpdef mutate(self):
	# Causes the Animal's genes to mutate
		cdef np.ndarray[double,ndim=1] new_genes = self.genes
		cdef int k
		cdef double r, mutation_step
		cdef double mu = self._constants["mu"]

		for k in [0,1,3,4,7]:
			r = randnum()
			if (r<=mu):
				mutation_step = np.random.normal(loc=0,scale=0.05)
				new_genes[k] += mutation_step
				
		if new_genes[1] > 0.5:
			for k in [2,5,6,8]:
				r = randnum()
				if (r<=mu):
					mutation_step = np.random.normal(loc=0,scale=0.05)
					new_genes[k] += mutation_step
		else:
			new_genes[2], new_genes[5], new_genes[6], new_genes[8] = 0, 0, 0, 0

		return new_genes

# PROTECTED METHODS

cdef inline double scale(double x):
# Defines the scale function, decreasing gene efficiency for extreme values
	if x < 0:
		return -1*c_log(c_abs(x)+1)/c_log(3)
	else:
		return c_log(c_abs(x)+1)/c_log(3)


cdef inline np.ndarray[double,ndim=1] random_genes():
# Returns random values for the 9 genes in the chosen intervals:
# h: 1, s: [0,1], a: [0,1], I0: [-1,1], I0p: [-1,1], b: [-2,2], bp: [-2,2], m: 0, ma: 0
	cdef np.ndarray[double,ndim=1] rand_numbers, rand_genes 
	rand_numbers = np.array([randnum() for _ in np.arange(9)])
	rand_genes = [0,1,1,2,2,4,4,0,0]*rand_numbers+[1,0,0,-1,-1,-2,-2,0,0]

	if (rand_genes[1]<=0.5):
		rand_genes[2], rand_genes[5], rand_genes[6], rand_genes[8] = 0, 0, 0, 0
	return rand_genes

cdef inline float randnum():
	return c_rand() / float(RAND_MAX)
