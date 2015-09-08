#########################################################
#	iterate_population.py
#	Author: Dion Häfner (dionhaefner@web.de)
#	
#	Main controller for a given population
#	
#	Licensed under BSD 2-Clause License
#########################################################


# Import third party libraries
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
import time

# Seaborn makes prettier plots, but is not installed in a fresh Anaconda python
try: 
	import seaborn as sns
	have_seaborn = True
except ImportError:
	have_seaborn = False

# Import other parts of the project
from animal import Animal
from population import Population
from environment import Environment
from constants import model_constants
from output_population import output_population, plot_size


def iterate_population(k,population,environments,f1,f2,path,t=0,variable=False):
# MAIN CONTROLLER
# Inputs:
#	k: population counter,	population: the Population instance to be iterated,
#	f1: pointer to output file for gene means, 	f2: for gene standard deviations,
#	path: path to the output files,	timeseries: output plotting in every timestep,
#	t: initial time,	variable: variable population size

	constants = model_constants
	timeseries = constants["timeseries"]
	nE = len(environments)

	for j in np.arange(constants["generations"]):
		start = time.clock()

		# output previous population
		output_population(population,f1,f2,j,k,path,timeseries,t,environments)

		###################################
		# THIS IS WHERE THE MAGIC HAPPENS #
		###################################

		for _ in range(constants["L"]):
			E, C = np.empty(nE), np.empty(nE)

			for (i,env) in enumerate(environments):
				E[i], C[i] = env.evaluate(t)

			population.react(E,C)
			t = t+1

		if variable:
			population.breed_variable()
		else:
			population.breed_constant()

		if population.size() == 0:
			print("Population died out!\n\n")
			return None, None, j

		population.react(E,C,1)

		# \end{magic}

		print("Pop {2}: Generation {0} of {1} done!".format(j+1,constants["generations"],k+1))
		end = time.clock()
		print("Computation time: {0:.3e} s\n".format(end-start))

	# Final outputs for each population
	final_mean, final_std = output_population(population,f1,f2,j,k,path,True,t,environments)
	f1.close()
	f2.close()

	plot_size(path,path+"pop"+str(k+1)+"_mean_genes.csv",k)

	return final_mean, final_std, j
