#########################################################
#	constants.py
#	Author: Dion Häfner (dionhaefner@web.de)
#	
#	Defining the constants of the Botero evolution model
#	
#	Licensed under BSD 2-Clause License
#########################################################


def model_constants():
	constants = {	
		"population_size": 		5000, # number of animals per population
		"generations": 			1000, # number of generations per run
		"L": 					5, 	  # time step lifetime of each animal
		"kd": 					0.02, # constant cost of plasticity
		"ka": 					0.01, # cost of each adaptation
		"tau": 					0.25, # coefficient of lifetime payoff exponential
		"q": 					2.2,  # controls number of offspring in variable scenario
		"mu":					0.00001,
		"environments":			[(0.1,0.6,0.,0.),
								(.7,1.0,0.,0.5),
								(.5,1.0,0.,-0.7)],
									  # parameters of each environment
									  # in the form (P,A,B,O)
		"environment_names":	["moderate",
								"warm",
								"cold"],
									  # name of each environment to be displayed
		"km":					0.2,  # cost of migration
		"limit":				["m"] # names of genes that should be limited to [0,1]
									  # candidates: h, s, a, m, ma
		}
	return constants
