#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
#########################################################
#
#	environment.py
#	Author: Dion Häfner (dionhaefner@web.de)
#	
#	Implementing Environment class and methods
#	
#	Licensed under BSD 2-Clause License
#
#########################################################
"""

import numpy as np

from constants import model_constants
import numbers


class Environment:
	def __init__(self,R,P,A,B,O,name=""):
		"""Creates an Environment instance with given properties"""
		if (all(isinstance(x,numbers.Number) for x in [R,P,A,B,O])):
			self.R = max(0,R)
			self.P = max(0,min(P,1))
			self.A = A
			self.B = B
			self.O = O
			self.name = name
			self._constants = model_constants
		else:
			raise TypeError('First five arguments must be numeric.')

	def evaluate(self,t):
		"""Returns environment value E and cue C for given time t"""
		epsilon = np.random.normal(0,float(1)/3)
		E = self.A * np.sin(2 * np.pi / self._constants["L"] / self.R * t) + self.B * epsilon + self.O
		mu, sigma = self.P*(E-self.O), float(1-self.P)/3
		if (sigma <= 0):
			C = mu
		else:
			C = np.random.normal(mu,sigma)
		return E,C
