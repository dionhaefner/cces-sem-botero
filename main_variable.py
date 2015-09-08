#!/usr/bin/env python

#########################################################
#	main_variable.py
#	Author: Dion Häfner (dionhaefner@web.de)
#	
#	Main controller, with variable population size
#	
#	Licensed under BSD 2-Clause License
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
import csv # For file operations

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

	f_mean = constants["mean_file"]
	f_std = constants["std_file"]

	# create output directory
	now = datetime.datetime.today()
	path = "./output_variable/{0}/{1:%y}-{1:%m}-{1:%d}_{1:%H}-{1:%M}-{1:%S}/".format(f_mean,now)
	try: 
		os.makedirs(path)
		os.makedirs(path+"timeseries/")
	except OSError:
		if not os.path.isdir(path):
			raise

	start = time.clock()

	# read the csv files
	nE = 0
	env = []
	with open(f_mean) as f:
		reader = csv.reader(f,delimiter=",")
		for (i,row) in enumerate(reader):
			if row:
				if i == 0:
					nE = int(row[0])
				elif row[0]=="n":
					data = np.genfromtxt(f_mean,skiprows=i+1,delimiter=",")
					break
				elif (row[0][0]!="R") & (i > 1):
					env.append(list(map(float,row)))
	mean_genes = data[-nE:,1:-1]
	sizes = data[-nE:,-1].reshape(nE)
	final_t = data[-1,0]*constants["L"]*env[0][0]/constants["environments"][0][0]

	data = np.genfromtxt(f_std,skiprows=i+1,delimiter=",")
	std_genes = data[-nE:,1:-1]
	std_genes = np.fabs(std_genes)

	# create environments
	environments = []
	for param in env:
		new_env = Environment(*param)
		environments.append(new_env)

	f3 = open(path+"__overview.txt",'w')
	f3.write("initial conditions \n")

	for (i,env) in enumerate(environments):
		f3.write("R{4},P{4},A{4},B{4},O{4}\n{0},{1},{2},{3},{5}\n".format(env.R,env.P,env.A,env.B,i,env.O))

	f3.write("{0}\n".format(mean_genes))
	f3.write("{0}\n".format(std_genes))
	f3.write("mu = {0}, q = {1} \n\n".format(constants["mu"],constants["q"]))


	end = time.clock()
	if constants["verbose"]:
		print("Set-up time: {0:.2e}s\n".format(end-start))
	start = time.clock()

	survival_rate = 0
	for k in range(constants["populations"]):
		# write starting genes in files

		f1 = open(path+"pop"+str(k+1)+"_mean_genes.csv",'w')
		f1.write("{0}\n\n".format(nE))
		f1.write("n,environment,I0,I0p,a,b,bp,h,s,m,ma,size\n")
		
		f2 = open(path+"pop"+str(k+1)+"_std_genes.csv",'w')
		f2.write("{0}\n\n".format(nE))
		f2.write("n,environment,I0,I0p,a,b,bp,h,s,m,ma,size\n")
			
		# create animals with the mean genes that shall be tested for each environment
		animals=[]
		for i in range(nE):
			if sizes[i] == 0:
				continue
			genes = []
			gene_order = [6,9,3,1,2,4,5,7,8]
			for j in gene_order:
				if (std_genes[i,j] > 0):
					genes.append(np.random.normal(size=sizes[i],loc=mean_genes[i,j],scale=std_genes[i,j]))
				else:
					genes.append(mean_genes[i,j]*np.ones(sizes[i]))
			animals.append([Animal(np.array(genes),i) for genes in zip(*genes)])
		animals = [item for sublist in animals for item in sublist]
			
		# create a population of population_size animals that have the correct mean genes
		population = Population(constants["population_size"],animals)
		
		
		f3.write("Population {0}".format(k+1))
		pop_mean, pop_std, final_gen = iterate_population(k,population,environments,f1,f2,path,final_t,True)
		end = time.clock()


		if pop_mean is None:
			if not constants["verbose"]:
				print("\n\tDied out! Total time: {0:.2f} min\n".format((end-start)/60)) 
			f3.write(" died at generation {0}!\n".format(final_gen))
		else:
			if not constants["verbose"]:
				print("\n\tSurvived! Total time: {0:.2f} min\n".format((end-start)/60)) 
			survival_rate = survival_rate+1
			f3.write(" survived!\n")

		if constants["verbose"]:
			print("\n---------------------------------------")
			print(" Population {0} done! Total time: {1:.2f} min".format(k+1,(end-start)/60))
			print("---------------------------------------\n")

	f3.write("\n\nIn total, {0}/{1} Populations survived.".format(survival_rate,constants["populations"]))
