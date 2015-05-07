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

try: # Seaborn makes prettier plots, but is not installed in a fresh Anaconda python
	import seaborn as sns 
	have_seaborn = True
except ImportError:
	have_seaborn = False

#
# Import other parts of the project
#

from popclasses import * # Import custom classes
from constants import model_constants # Import model constants
from environment import * # Environment model
from iterate_population import iterate_population # Main controller for population iteration





# Get model constants
constants = model_constants()

# Get parameters from command line
arguments = sys.argv[1:]
if (len(arguments) != 6):
	print("Usage: main.py [populations] [R] [P] [A] [B] [output timeseries]")
	print("E.g. $ python main.py 100 1 0 1 0 0")
	sys.exit(0)
else:
	try:
		populations, timeseries = int(arguments[0]), arguments[5].lower() in ("true", "t", "1", "True")
		R, P, A, B = list(map(float,arguments[1:5]))
	except ValueError:
		print("Usage: main.py [populations] [R] [P] [A] [B] [output timeseries]")
		print("E.g. $ python main.py 100 1 0 1 0 0\n")
		raise


if __name__ == '__main__':
	if have_seaborn: # initialize seaborn
		sns.set_palette("deep", desat=.6)
		sns.set_context(rc={"figure.figsize": (10, 7.5)})

	# create output directory
	now = datetime.datetime.today()
	path = "./output/R{0}-P{1}-A{2}-B{3}_{4:%y}-{4:%m}-{4:%d}_{4:%H}-{4:%M}-{4:%S}/".format(R,P,A,B,now)
	try: 
		os.makedirs(path)
		os.makedirs(path+"timeseries/")
	except OSError:
		if not os.path.isdir(path):
			raise

	# plot environment
	plt.figure()
	t0 = np.arange(0,R*100,float(R)/10)
	env = np.array(list(map(lambda x: environment(x,R,P,A,B),t0)))
	plt.plot(t0,env[:,0],label='E')
	plt.plot(t0,env[:,1],'.',label='C')
	plt.legend()
	plt.savefig(path+'environment.png')

	plt.figure()
	plt.hist(env[:,1],bins=100)
	plt.savefig(path+'cues.png')

	means, stds = [], []
	for k in range(populations):
		start = time.clock()

		# create a population of population_size animals that already have the correct random genes
		animal_list = [Animal() for _ in range(constants["population_size"])]

		# create a Population from animal_list
		population = Population(constants["population_size"],animal_list)

		end = time.clock()
		print("Set-up time: {0}\n".format(end-start))
		start = time.clock()
		
		# iterate on the population and create outputs
		pop_mean, pop_std = iterate_population(k,population,R,P,A,B,path,timeseries)

		end = time.clock()
		print("\n---------------------------------------")
		print(" Population {0} done! Total time: {1:.2f} min".format(k+1,(end-start)/60))
		print("---------------------------------------\n")

		plt.close('all')

		means.append(pop_mean)
		stds.append(pop_std)

	plt.figure()
	average = pd.concat(means)
	if have_seaborn:
		sns.violinplot(average)
	else:
		average.boxplot()
	plt.ylim(-2,2)
	plt.savefig(path+"total_average.png")
	plt.close()