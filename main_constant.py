#!/usr/bin/env python
# -*- coding: utf8 -*-

#########################################################
#
#	main_constant.py
#	Author: Dion Häfner (dionhaefner@web.de)
#	
#	Main controller, with constant population size
#
#	Usage:
#		python main_constant.py [options]
#
#	Licensed under BSD 2-Clause License
#
#########################################################

import sys
sys.path.insert(0, './src')

#
# Import third-party packages
#

import numpy as np # For efficient array operations
import matplotlib.pyplot as plt # For plotting
import time # For timing parts of the script, optimizing run time
import pandas as pd # Easier data handling
import os # To create directories
import datetime # To access the current time
import sys # To access command line arguments
import warnings # To warn the user

try: # Seaborn makes prettier plots, but is not installed in a fresh Anaconda python
	import seaborn as sns 
	have_seaborn = True
except ImportError:
	have_seaborn = False

#
# Import other parts of the project
#

from animal import Animal
from population import Population
from environment import Environment
from constants import model_constants
from iterate_population import iterate_population



if __name__ == '__main__':
	# Get model constants
	constants = model_constants

	if have_seaborn: # initialize seaborn
		sns.set('poster')
		sns.set_palette("deep", desat=.6)
		sns.set_context(rc={"figure.figsize": (10, 7.5)})

	# create output directory
	now = datetime.datetime.today()
	path = "./output/{0:%y}-{0:%m}-{0:%d}_{0:%H}-{0:%M}-{0:%S}/".format(now)
	try: 
		os.makedirs(path)
		os.makedirs(path+"timeseries/")
	except OSError:
		if not os.path.isdir(path):
			raise

	# write simulation parameters
	f = open(path+"parameters.txt","w")
	for key in constants:
		f.write("{0}:\t{1}\n".format(key,constants[key]))

	# plot environments
	t0 = np.arange(0,constants["L"]*constants["generations"])

	environments = []
	for (i,param) in enumerate(constants["environments"]):
		new_env = Environment(*param)
		environments.append(new_env)
		env_val = np.array(list(map(new_env.evaluate,t0)))

		plt.figure()
		plt.plot(t0,env_val[:,0],label='E')
		plt.plot(t0,env_val[:,1],'.',label='C')
		plt.legend()
		plt.ylim(-2,2)
		plt.savefig(path+'environment_'+str(i+1)+'.png',bbox_inches='tight')

	# main loop over multiple populations
	nE = len(environments)
	means, stds = [], []
	error_occured = False
	for k in range(constants["populations"]):
		start = time.clock()

		# in case a population dies out, it is repeated
		repeat = True
		while repeat:
			# create a population of population_size animals that already have the correct random genes
			animal_list = [Animal() for _ in range(constants["population_size"])]
			# create a Population from animal_list
			population = Population(constants["population_size"],animal_list)

			end = time.clock()
			if constants["verbose"]:
				print("Set-up time: {0:.2e}s\n".format(end-start))
			start = time.clock()

			# initial output
			f1 = open(path+"pop"+str(k+1)+"_mean_genes.csv",'w')
			f2 = open(path+"pop"+str(k+1)+"_std_genes.csv",'w')

			f1.write("{0}\n\n".format(nE))
			f2.write("{0}\n\n".format(nE))
			
			for (i,env) in enumerate(environments):
				f1.write("R{4},P{4},A{4},B{4},O{4}\n{0},{1},{2},{3},{5}\n".format(env.R,env.P,env.A,env.B,i,env.O))
				f2.write("R{4},P{4},A{4},B{4},O{4}\n{0},{1},{2},{3},{5}\n".format(env.R,env.P,env.A,env.B,i,env.O))

			f1.write("\nn,I0,I0p,a,b,bp,h,s,m,ma\n")
			f2.write("\nn,I0,I0p,a,b,bp,h,s,m,ma\n")
					
			# iterate on the population and create outputs
			try:
				pop_mean, pop_std, _ = iterate_population(k,population,environments,f1,f2,path)
				repeat = False
			except RuntimeError:
				error_occured = True
				pass


		end = time.clock()
		if constants["verbose"]:
			print("\n---------------------------------------")
			print(" Population {0} done! Total time: {1:.2f} min".format(k+1,(end-start)/60))
			print("---------------------------------------\n")
		else:
			print("\n\tDone! Total time: {0:.2f} min\n".format((end-start)/60))

		plt.close('all')

		means.append(pop_mean)
		stds.append(pop_std)

	# plot average genes of ALL populations run
	for i in range(len(constants["environments"])):
		mean_i = [mean[i] for mean in means]
		plt.figure()
		average = pd.concat(mean_i)
		if have_seaborn:
			sns.violinplot(data=average,scale='width')
		else:
			average.boxplot()
		plt.ylim(-2,2)
		plt.savefig(path+"total_average_env_"+str(i+1)+".png",bbox_inches='tight')
		plt.close()

	if error_occured:
		warnings.warn("At least one population died out and was repeated!")
