#
# Import packages
#

import numpy as np # For efficient array operations
import matplotlib.pyplot as plt # For plotting
import time # For timing parts of the script, optimizing run time
import pandas as pd # Easier data handling
import os # To create directories
import datetime # To access the current time
import sys # To access command line arguments
import warnings

try: # Seaborn makes prettier plots, but is not installed in a fresh Anaconda python
	import seaborn as sns 
	have_seaborn = True
except ImportError:
	have_seaborn = False

#
# Import other parts of the project
#

# Import custom classes
from genome import Genome 
from animal import Animal
from population import Population

from constants import model_constants # Import model constants
from environment import * # Environment model
from iterate_population import iterate_population # Main controller for population iteration


# Get model constants
constants = model_constants()

# Get parameters from command line
arguments = sys.argv[1:]
if (len(arguments) != 3):
	print("Usage: main.py [populations] [R] [output timeseries]")
	print("E.g. $ python main.py 100 1E4 1")
	sys.exit(0)
else:
	try:
		populations, R, timeseries = int(arguments[0]), float(arguments[1]), arguments[2].lower() in ("true", "t", "1")
	except ValueError:
		print("Usage: main.py [populations] [R] [output timeseries]")
		print("E.g. $ python main.py 100 1E4 1\n")
		raise


if __name__ == '__main__':
	if have_seaborn: # initialize seaborn
		sns.set('poster')
		sns.set_palette("deep", desat=.6)
		sns.set_context(rc={"figure.figsize": (10, 7.5)})

	# create output directory
	now = datetime.datetime.today()
	path = "./output/R{1}-{0:%y}-{0:%m}-{0:%d}_{0:%H}-{0:%M}-{0:%S}/".format(now,R)
	try: 
		os.makedirs(path)
		os.makedirs(path+"timeseries/")
	except OSError:
		if not os.path.isdir(path):
			raise

	# plot environment
	t0 = np.arange(0,constants["L"]*constants["generations"])

	environments = []
	for (i,param) in enumerate(constants["environments"]):
		new_env = Environment(R,*param)
		environments.append(new_env)
		env_val = np.array(list(map(new_env.evaluate,t0)))

		plt.figure()
		plt.plot(t0,env_val[:,0],label='E')
		plt.plot(t0,env_val[:,1],'.',label='C')
		plt.legend()
		plt.ylim(-2,2)
		plt.savefig(path+'environment_'+str(i+1)+'.png',bbox_inches='tight')

	means, stds = [], []
	error_occured = False
	for k in range(populations):
		start = time.clock()

		repeat = True
		while repeat:
			# create a population of population_size animals that already have the correct random genes
			animal_list = [Animal() for _ in range(constants["population_size"])]

			# create a Population from animal_list
			population = Population(constants["population_size"],animal_list)

			end = time.clock()
			print("Set-up time: {0:.2e}s\n".format(end-start))
			start = time.clock()
			
			# iterate on the population and create outputs
			try:
				pop_mean, pop_std = iterate_population(k,population,environments,path,timeseries)
				repeat = False
			except RuntimeError:
				error_occured = True
				pass


		end = time.clock()
		print("\n---------------------------------------")
		print(" Population {0} done! Total time: {1:.2f} min".format(k+1,(end-start)/60))
		print("---------------------------------------\n")

		plt.close('all')

		means.append(pop_mean)
		stds.append(pop_std)

	for i in range(len(constants["environments"])):
		mean_i = [mean[i] for mean in means]
		plt.figure()
		average = pd.concat(mean_i)
		if have_seaborn:
			sns.violinplot(average)
		else:
			average.boxplot()
		plt.ylim(-2,2)
		plt.savefig(path+"total_average_env_"+str(i+1)+".png",bbox_inches='tight')
		plt.close()

	if error_occured:
		warnings.warning("At least one population died out and was repeated! Check outputs.")