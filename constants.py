from collections import namedtuple

def model_constants():
	Constants = namedtuple('Constants', ['population_size', 'generations', 'L', 'kd', 'ka', 'tau', 'q', 'mu'])
	constants = Constants(5000, 1000, 5, 0.02, 0.01, 0.25, 2.2, 0.001)
	return constants
