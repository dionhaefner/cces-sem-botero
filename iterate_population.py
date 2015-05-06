
import numpy as np # For efficient array operations
import matplotlib.pyplot as plt # For plotting
import pandas as pd # Easier data handling
import time # For timing parts of the script, optimizing run time

try: # Seaborn makes prettier plots, but is not installed in a fresh Anaconda python
	import seaborn as sns 
	have_seaborn = True
except ImportError:
	have_seaborn = False

from popclasses import * # Import custom classes
from constants import model_constants # Import model constants
from environment import * # Environment model
constants = model_constants()

def output_population(population,f1,f2,j,k,path,timeseries):
	animals = population.animals()
	genes = list(map(lambda x: x.genes, animals))
	data = pd.DataFrame(genes)
	mean = pd.DataFrame(data.mean()).transpose()
	std = pd.DataFrame(data.std()).transpose()
	f1.write(str(j)+","); f2.write(str(j)+",")
	mean.to_csv(f1, header=False, index=False)
	std.to_csv(f2, header=False, index=False)

	if timeseries:
		plt.figure()
	
		if have_seaborn:
			sns.violinplot(data)
		else:
			data.boxplot()
	
		plt.ylim(-2,2)
		plt.savefig(path+'timeseries/pop'+str(k+1)+'_genes_'+str(j)+'.png')
		plt.close()

def iterate_population(k,population,R,P,A,B,path,timeseries=False):
	t = 0; 

	f1 = open(path+"pop"+str(k+1)+"_mean_genes.csv",'w')
	f1.write("R,P,A,B\n{0},{1},{2},{3}\nn,I0,I0p,a,b,bp,h,s\n".format(R,P,A,B))

	f2 = open(path+"pop"+str(k+1)+"_std_genes.csv",'w')
	f2.write("R,P,A,B\n{0},{1},{2},{3}\nn,I0,I0p,a,b,bp,h,s\n".format(R,P,A,B))

	for j in np.arange(constants["generations"]):
		# Start timer
		start = time.clock()

		# output previous population
		output_population(population,f1,f2,j,k,path,timeseries)

		###################################
		# THIS IS WHERE THE MAGIC HAPPENS #
		###################################

		for i in range(constants["L"]):

			E, C = environment(t,R,P,A,B)
			population.react(E,C)
			t = t+1

		population.breed_constant()
		population.react(E,C,1)

		# \end{magic}

		print("Pop {2}: Generation {0} of {1} done!".format(j+1,constants["generations"],k+1))
		end = time.clock()
		print("Computation time: {0:.3e} s\n".format(end-start))

	# Final outputs

	output_population(population,f1,f2,j,k,path,True)

	I0, b, I0p, bp = [], [], [], []
	for animal in population.animals():
		I0.append(animal.genes['I0'])
		b.append(animal.genes['b'])
		I0p.append(animal.genes['I0p'])
		bp.append(animal.genes['bp'])

	I0, b = np.array(I0), np.array(b)
	C = np.linspace(-1,1,200)

	plt.figure()
	plt.plot(C,np.mean(I0)+np.mean(b)*C)
	plt.plot(C,np.mean(I0p)+np.mean(bp)*C)
	plt.savefig(path+'pop'+str(k+1)+'_mean.png')