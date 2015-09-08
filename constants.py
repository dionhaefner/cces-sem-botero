# -*- coding: utf8 -*-
#########################################################
#	constants.py
#	Author: Dion Häfner (dionhaefner@web.de)
#	
#	Defining the constants of the Botero evolution model
#	and parsing them from command line.
#	
#	Licensed under BSD 2-Clause License
#########################################################

import argparse

# SETS AVAILABLE MODEL PARAMETERS, THEIR TYPE, DEFAULT VALUE AND DESCRIPTION
_PARAMETERS = [
			("population_size",int,5000,"number of animals per population"),
			("generations",int,1000,"number of generations per run"),
			("L",int,5,"life time of each animal in time steps"),
			("kd",float,0.02,"constant cost of plasticity"),
			("ka",float,0.01,"cost of each adaptation"),
			("tau",float,0.25,"coefficient of lifetime payoff exponential"),
			("q",float,2.2,"controls expected number of offspring in variable scenario"),
			("mu",float,1E-3,"mutation rate of the genes"),
			("environments",float,[[1E2,0.1,0.6,0.,0.],
						[1E2,.7,1.0,0.,0.5],
						[1E2,.5,1.0,0.,-0.7]], "parameters of each environment "+
                                                		            "in the form R P A B O)"),
			("environment_names",str,["moderate",
							"warm",
							"cold"],"displayed name of each environment"),
			("km",float,0.2,"cost of migration"),
			("limit",str,"m","names of genes that should be limited to [0,1]"),
			("populations",int,1,"number of identical populations per run"),
			("timeseries",bool,False,"whether detailed output is given in every time step")
		]


# Implement class for containing constants
class ModelConstants(dict):
	def __init__(self):
		super(ModelConstants,self).__init__()
		for param in _PARAMETERS:
			self[param[0]] = param[2]
			
	def change_constant(self,key,val):
		if key in self:
			self[key] = val
		else:
			raise KeyError("Key {0} is not a valid model constant identifier!".format(key))


# Parse parameters from command line
model_constants = ModelConstants()
parser = argparse.ArgumentParser()

for key in _PARAMETERS:
	if key[0] in ["environments"]:
		Nenv = len(key[2])
		parser.add_argument("--"+key[0],type=key[1],action="append",nargs=5,help=key[3])
	elif key [0] in ["environment_names","limit"]:
		parser.add_argument("--"+key[0],type=key[1],action="append",nargs="*",help=key[3])
	else:
		parser.add_argument("--"+key[0],type=key[1],help=key[3])
for key in ["R","P","A","B","O"]:
	parser.add_argument("--"+key,type=int,nargs=Nenv,help="Overrides parameter {0} for each environment".format(key))

args = parser.parse_args().__dict__

for key in _PARAMETERS:
	if args[key[0]]:
		model_constants.change_constant(key[0],args[key[0]])
for i,key in enumerate(["R","P","A","B","O"]):
	environments = model_constants["environments"]
	if args[key]:
		for env in environments:
			env[i] = args[key][i]


