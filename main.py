# Import packages
import numpy as np # For efficient array operations
import matplotlib as mpl
import matplotlib.pyplot as plt # For plotting
#import seaborn as sns # Makes prettier plots
import time # For timing parts of the script, optimizing run time
import profile
import pandas as pd

# Import other parts of the project
from popclasses import * # Import custom classes
from constants import model_constants # Import model constants
from environment import * # Import environment model



if __name__ == '__main__':
	#sns.set_palette("deep", desat=.6)
	#sns.set_context(rc={"figure.figsize": (10, 7.5)})

	#################################
	############# START #############
	#################################


	# Get model constants
	constants = model_constants()

	# Now lets create a population of population_size animals that already have the correct random genes:
	animal_list = [Animal() for _ in range(constants.population_size)]

	# create a Population from animal_list
	population = Population(constants.population_size,animal_list)

	# set some variable model parameters:
	t, R, P, A, B = 0, 100, 1, 1, 0

	plt.figure()
	t0 = np.arange(0,R*100,float(R)/10)
	env = np.array(list(map(lambda x: environment(x,R,P,A,B),t0)))
	plt.plot(t0,env[:,0],label='E')
	plt.plot(t0,env[:,1],'.',label='C')
	plt.legend()
	plt.savefig('environment.png')

	plt.figure()
	plt.hist(env[:,1],bins=100)
	plt.savefig('cues.png')

	for j in np.arange(constants.generations):
		# Start timer
		start = time.clock()

		for i in range(constants.L):

			E, C = environment(t,R,P,A,B)
			population.react(E,C)
			t = t+1

		population.breed_constant()
		population.react(E,C,1)

		plt.figure()
		animals = population.animals()
		genes = list(map(lambda x: x.genes, animals))
		data = pd.DataFrame(genes)
		data.boxplot()
		plt.ylim(-2,2)
		plt.savefig('timeseries/genes_'+str(j+1)+'.png')
		plt.close()


		print("Generation {0} of {1} done!".format(j+1,constants.generations))
		end = time.clock()
		print("Computation time: {0:.3e} s".format(end-start))



	I0, b, I0p, bp = [], [], [], []
	for animal in population.animals():
		I0.append(animal.genes['I0'])
		b.append(animal.genes['b'])
		I0p.append(animal.genes['I0p'])
		bp.append(animal.genes['bp'])

	I0, b = np.array(I0), np.array(b)
	data = np.vstack((I0,b)).T

	C = np.linspace(-1,1,200)

	data = pd.DataFrame(data, columns=["I0", "b"])
	# sns.kdeplot(data)
	# sns.plt.show()

	sns.jointplot("I0", "b", data, kind='hex')
	sns.plt.savefig('kde.png')

	plt.figure()
	plt.scatter(I0,b)
	plt.savefig('scatter.png')

	plt.figure()
	plt.plot(C,np.mean(I0)+np.mean(b)*C)
	plt.plot(C,np.mean(I0p)+np.mean(bp)*C)
	plt.savefig('mean.png')
