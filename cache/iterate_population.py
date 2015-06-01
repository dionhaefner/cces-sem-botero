import numpy as np # For efficient array operations
import matplotlib.pyplot as plt # For plotting
import pandas as pd # Easier data handling
import time # For timing parts of the script, optimizing run time

# Seaborn makes prettier plots, but is not installed in a fresh Anaconda python
try: 
	import seaborn as sns 
	have_seaborn = True
except ImportError:
	have_seaborn = False

# Import custom classes
from genome import Genome 
from animal import Animal
from population import Population

from constants import model_constants # Import model constants
from environment import * # Environment class
from output_population import output_population, plot_size
constants = model_constants()


def iterate_population(k,population,environments,path,timeseries):
	t = 0;

	f1 = open(path+"pop"+str(k+1)+"_mean_genes.csv",'w')
	f2 = open(path+"pop"+str(k+1)+"_std_genes.csv",'w')

	for (i,env) in enumerate(environments):
		f1.write("R{4},P{4},A{4},B{4}\n{0},{1},{2},{3}\n".format(env.R,env.P,env.A,env.B,i))
		f2.write("R{4},P{4},A{4},B{4}\n{0},{1},{2},{3}\n".format(env.R,env.P,env.A,env.B,i))

	f1.write("\nn,I0,I0p,a,b,bp,h,s\n")
	f2.write("\nn,I0,I0p,a,b,bp,h,s\n")

	nE = len(environments)

	for j in np.arange(constants["generations"]):
		# Start timer
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

		population.breed_constant()

		if population.size() == 0:
			print("Population died out!\n\n")
			return

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

	I0, b, I0p, bp, h = [], [], [], [], []
	for animal in population.animals():
		I0.append(animal.genes['I0'])
		b.append(animal.genes['b'])
		I0p.append(animal.genes['I0p'])
		bp.append(animal.genes['bp'])
		h.append(animal.genes['h'])

	C = np.linspace(-1,1,200)

	mean_h = np.mean(h)

	plt.figure()
	plt.plot(C,np.mean(I0)+np.mean(b)*C,alpha=mean_h,label='$I_0$ and $b$')
	plt.plot(C,np.mean(I0p)+np.mean(bp)*C,alpha=(1-mean_h),label="$I_0'$ and $b'$")
	plt.legend(loc='best')
	plt.ylim(-2,2)
	plt.savefig(path+'pop'+str(k+1)+'_mean.png')

	return final_mean, final_std