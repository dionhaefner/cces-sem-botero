# -*- coding: utf8 -*-
"""
#########################################################
#
#	animal.pyx
#	Author: Dion Häfner (dionhaefner@web.de)
#
#	Implements animal class and methods
#	(cythonized version of animal.py and genome.py)
#
#	YOU WILL NEED TO RUN setup.py AFTER MAKING CHANGES HERE
#
#	Licensed under BSD 2-Clause License
#
#########################################################
"""

import numpy as np

from constants import model_constants

# imports from c libraries for speed
cimport numpy as np
from libc.math cimport abs as c_abs
from libc.math cimport log as c_log
from libc.math cimport exp as c_exp
from libc.stdlib cimport rand as c_rand
from libc.stdlib cimport RAND_MAX
from libc.math cimport fmax as c_max
from libc.math cimport fmin as c_min

# custom type definitions
FTYPE = np.double
DTYPE = np.int
BTYPE = np.uint8
ctypedef np.float_t FTYPE_t
ctypedef np.int_t DTYPE_t
ctypedef np.uint8_t BTYPE_t

cdef int nE = len(model_constants["environments"])



cdef class Animal:
	"""Implements a cython class Animal, that is also available outside of this module"""
	# properties of Animal, typed as C variables for speed
	cdef object _constants
	cdef FTYPE_t h,s,a,I0,I0p,b,bp,m,ma
	cdef DTYPE_t adjustments
	cdef DTYPE_t migrations
	cdef FTYPE_t insulation
	cdef BTYPE_t primed
	# public keyword makes the variable accessible to python
	cdef public FTYPE_t mismatch
	cdef public DTYPE_t position

	def __init__(self,np.ndarray[double,ndim=1] parent_genes=np.array([]),int position=nE+1):
		"""Constructor"""
		self._constants = model_constants
		if not parent_genes.size: # empty argument -> random genes (default)
			self.genes = random_genes()
		else:
			self.genes = parent_genes
		if position > nE: # too large argument -> random position (default)
			position = np.random.randint(nE)
		self.mismatch = 0
		self.adjustments = 0
		self.migrations	= 0
		self.insulation = self.genes[3]
		self.position = position
		r = randnum()
		if (r <= self.h):
			self.primed = 0
		else:
			self.primed = 1

# PUBLIC METHODS

	cpdef react(self,np.ndarray[double,ndim=1] E,np.ndarray[double,ndim=1] C,BTYPE_t evolve_all=0):
		"""Animal migrates and reacts to environment E and cue C. If evolve_all is set, reaction takes place for all animals, regardless of gene 'a'."""
		cdef np.ndarray[DTYPE_t,ndim=1] positions
		cdef DTYPE_t new_position
		cdef FTYPE_t new_insulation
		cdef FTYPE_t r

		r = randnum()
		if ((r <= self.ma) | evolve_all) & (nE > 1):
			r = randnum()
			if (r <= self.m):
				positions = np.arange(nE)
				new_position = np.random.choice(positions[positions!=self.position])
				self.position = new_position
				self.migrations += 1

		r = randnum()
		if ((r <= self.a) | evolve_all):
			if self.primed:
				new_insulation = scale(self.I0p)+scale(self.bp)*C[self.position]
			else:
				new_insulation = scale(self.I0)+scale(self.b)*C[self.position]

			self.insulation = new_insulation
			self.adjustments += 1

		self.mismatch = self.mismatch + c_abs(self.insulation-E[self.position])


	cpdef lifetime_payoff(self,np.ndarray[DTYPE_t] positions):
		"""Assembles the lifetime payoff of the animal"""
		cdef FTYPE_t scale_factor
		cdef FTYPE_t tau = self._constants["tau"]
		if len(positions) > 1:
			scale_factor = 1 - positions[self.position] / self._constants["population_size"]
		else:
			scale_factor = 1
		if (self.s <= 0.5):
			return scale_factor * c_max(c_exp(-tau*self.mismatch) - self._constants["km"] * self.migrations, 0)
		else:
			return scale_factor * c_max(c_exp(-tau*self.mismatch) - self._constants["kd"] \
				- self.adjustments * self._constants["ka"] - self._constants["km"] * self.migrations, 0)


	cpdef mutate(self):
		"""Causes the Animal's genes to mutate"""
		cdef np.ndarray[FTYPE_t,ndim=1] new_genes = self.genes
		cdef DTYPE_t k
		cdef FTYPE_t r, mutation_step
		cdef FTYPE_t mu = self._constants["mu"]

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



	property gene_dict:
		"""Allows the genes of the animal to be read from python as a dict by calling animal.gene_dict"""
		def __get__(self):
			return {"h":self.h,"s":self.s,"a":self.a,"I0":self.I0,"I0p":self.I0p,"b":self.b,"bp":self.bp,"m":self.m,"ma":self.ma}

	property genes:
		"""Allows the genes of the animal to be read and written from python as a list by calling animal.genes"""
		def __get__(self):
			return np.array([self.h,self.s,self.a,self.I0,self.I0p,self.b,self.bp,self.m,self.ma])

		def __set__(self, object genes):
			self.set_genes(genes)

	cdef set_genes(self,np.ndarray[double,ndim=1] genes):
		"""Checks every single gene if it is being limited or not. This may look messy, but is much faster than any loop implementation."""

		if not ("h" in self._constants["limit"]):
			self.h = genes[0]
		else:
			self.h = c_max(0,c_min(1,genes[0]))

		if not ("s" in self._constants["limit"]):
			self.s = genes[1]
		else:
			self.s = c_max(0,c_min(1,genes[1]))

		if not ("a" in self._constants["limit"]):
			self.a = genes[2]
		else:
			self.a = c_max(0,c_min(1,genes[2]))

		if not ("I0" in self._constants["limit"]):
			self.I0 = genes[3]
		else:
			self.I0 = c_max(0,c_min(1,genes[3]))

		if not ("I0p" in self._constants["limit"]):
			self.I0p = genes[4]
		else:
			self.I0p = c_max(0,c_min(1,genes[4]))

		if not ("b" in self._constants["limit"]):
			self.b = genes[5]
		else:
			self.b = c_max(0,c_min(1,genes[5]))

		if not ("bp" in self._constants["limit"]):
			self.bp = genes[6]
		else:
			self.bp = c_max(0,c_min(1,genes[6]))

		if not ("m" in self._constants["limit"]):
			self.m = genes[7]
		else:
			self.m = c_max(0,c_min(1,genes[7]))

		if not ("ma" in self._constants["limit"]):
			self.ma = genes[8]
		else:
			self.ma = c_max(0,c_min(1,genes[8]))


# PROTECTED FUNCTIONS

cdef inline double scale(double x):
	"""Defines the scale function, decreasing gene efficiency for extreme values"""
	if x < 0:
		return -1*c_log(c_abs(x)+1)/c_log(3)
	else:
		return c_log(c_abs(x)+1)/c_log(3)


cdef inline np.ndarray[double,ndim=1] random_genes():
	"""Returns random values for the 9 genes in the chosen intervals:
	h: 1, s: [0,1], a: [0,1], I0: [-1,1], I0p: [-1,1], b: [-2,2], bp: [-2,2], m: 0, ma: 0"""
	cdef np.ndarray[FTYPE_t,ndim=1] rand_numbers, rand_genes
	rand_numbers = np.array([randnum() for _ in np.arange(9)])
	rand_genes = [0,1,1,2,2,4,4,0,0]*rand_numbers+[1,0,0,-1,-1,-2,-2,0,0]

	if (rand_genes[1]<=0.5):
		rand_genes[2], rand_genes[5], rand_genes[6], rand_genes[8] = 0, 0, 0, 0
	return rand_genes

cdef inline double randnum():
	"""Returns random numbers at C speed"""
	return c_rand() / float(RAND_MAX)
