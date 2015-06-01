import numpy as np
from constants import model_constants
import numbers

constants = model_constants()

class Environment:
	def __init__(self,R,P,A,B,O,name=""):
		if (all(isinstance(x,numbers.Number) for x in [R,P,A,B,O])):
			self.R = R
			self.P = P
			self.A = A
			self.B = B
			self.O = O
			self.name = name
		else:
			raise TypeError('First five arguments must be numeric.')

	def evaluate(self,t):
		epsilon = np.random.normal(0,float(1)/3)
		E = self.A * np.sin(2 * np.pi / constants["L"] / self.R * t) + self.B * epsilon + self.O
		mu, sigma = self.P*(E-self.O)+self.O, float(1-self.P)/3
		if (sigma == 0):
			C = mu
		else:
			C = np.random.normal(mu,sigma)
		return E,C