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

from genome import Genome 
from animal import Animal
from population import Population
from environment import Environment
from constants import model_constants
from iterate_population import iterate_population



def main(f_mean,f_std,nR,nP,populations,timeseries):

	# Get model constants
	constants = model_constants()

	# create output directory
	now = datetime.datetime.today()
	path = "./output_var/{3}/R{0}-P{1}_{2:%y}-{2:%m}-{2:%d}_{2:%H}-{2:%M}-{2:%S}/".format(nR,nP,now,f_mean)
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
	final_t = data[-1,0]*constants["L"]*env[0][0]/nR

	data = np.genfromtxt(f_std,skiprows=i+1,delimiter=",")
	std_genes = data[-nE:,1:-1]
	std_genes = np.fabs(std_genes)

	# create environments
	environments = []
	for i in range(nE):
		new_env = Environment(*env[i])
		new_env.R = nR
		new_env.P += nP
		environments.append(new_env)


	f3 = open(path+"__overview.txt",'w')
	f3.write("initial conditions \n")

	for (i,env) in enumerate(environments):
		f3.write("R{4},P{4},A{4},B{4},O{4}\n{0},{1},{2},{3},{5}\n".format(env.R,env.P,env.A,env.B,i,env.O))

	f3.write("{0}\n".format(mean_genes))
	f3.write("{0}\n".format(std_genes))
	f3.write("mu = {0}, q = {1} \n\n".format(constants["mu"],constants["q"]))


	end = time.clock()
	print("Set-up time: {0:.2f} min\n".format((end-start)/60))
	start = time.clock()

	survival_rate = 0
	for k in range(populations):
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
			animals.append([Animal(Genome(genes),i) for genes in zip(*genes)])
		animals = [item for sublist in animals for item in sublist]
			
		# create a population of population_size animals that have the correct mean genes
		population = Population(constants["population_size"],animals)
		
		
		f3.write("Population {0}".format(k+1))
		pop_mean, pop_std, final_gen = iterate_population(k,population,environments,f1,f2,path,timeseries,final_t,True)
		if pop_mean is None:
			f3.write(" died at generation {0}!\n".format(final_gen))
		else:
			survival_rate = survival_rate+1
			f3.write(" survived!\n")
		end = time.clock()
		print("\n---------------------------------------")
		print(" Population {0} done! Total time: {1:.2f} min".format(k+1,(end-start)/60))
		print("---------------------------------------\n")

	f3.write("\n\nIn total, {0}/{1} Populations survived.".format(survival_rate,populations))



if __name__ == '__main__':
	# Get parameters from command line
	arguments = sys.argv[1:]
	if (len(arguments) !=6):
		print("Usage: main_variable.py [mean file] [std file] [nR] [nP] [n] [timeseries]")
		print("E.g. $ python main_variable.py mean.csv std.csv 1.1E4 0.5 10 False")
		sys.exit(0)
	else:
		try:
			f_mean, f_std = arguments[0:2]
			nR = float(arguments[2])
			nP = float(arguments[3])
			populations = int(arguments[4])
			timeseries = arguments[5].lower() in ("true", "t", "1")
				
		except ValueError:
			print("Usage: main_variable.py [mean file] [std file] [nR] [nP] [n] [timeseries]")
			print("E.g. $ python main_variable.py mean.csv std.csv 1.1E4 0.5 10 False\n")
			raise
	main(f_mean,f_std,nR,nP,populations,timeseries)