import numpy as np
from constants import model_constants

constants = model_constants()

def environment(t,R,P,A,B):
	epsilon = np.random.normal(0,float(1)/3)
	E = A * np.sin(2 * 3.1415 / constants["L"] / R * t) + B * epsilon
	mu, sigma = P*E, float(1-P)/3
	if (sigma == 0):
		C = mu
	else:
		C = np.random.normal(mu,sigma)

	return E,C