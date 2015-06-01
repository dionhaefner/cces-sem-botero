import numpy as np # For efficient array operations
import matplotlib.pyplot as plt # For plotting
import pandas as pd # Easier data handling
from copy import copy

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
constants = model_constants()


def output_population(population,f1,f2,j,k,path,timeseries,t,env):
	animals 	= np.array(population.animals())
	positions	= np.array(list(map(lambda x: x.position, animals)))

	nE 		= len(constants["environments"])
	genes 	= [list(map(lambda x: x.genes, animals[positions==i])) for i in range(nE)]
	nPerPos	= np.array([len(genes[i]) for i in range(nE)])
	data 	= [pd.DataFrame(genes[i]) for i in range(nE)]
	mean 	= [pd.DataFrame(data[i].mean()).transpose() for i in range(nE)]
	std		= [pd.DataFrame(data[i].std()).transpose() for i in range(nE)]


	for i in range(nE):
		f1.write(str(j)+","+str(i+1)+",")
		f2.write(str(j)+","+str(i+1)+",")
		mean[i].to_csv(f1, header=False, index=False, line_terminator='')
		std[i].to_csv(f2, header=False, index=False, line_terminator='')

		f1.write(","+str(nPerPos[i]))
		f2.write(","+str(nPerPos[i]))

		f1.write("\n")
		f2.write("\n")

	if timeseries:
		plt.figure(figsize=(20,15))
		ax = plt.subplot2grid((5,nE),(0,0),colspan=nE)
		if have_seaborn:
			palette = sns.color_palette("Set2", 3)
			names = np.array(constants["environment_names"])
			foo = pd.DataFrame({'env': names, 'val': nPerPos})
			sns.barplot('env','val',data=foo,ax=ax,palette=palette,x_order=names)
			ax.set_xlabel("")
			ax.set_ylabel("")
		else:
			ax.bar(np.array(constants["environment_names"]),nPerPos,0.7)
		ax.set_ylim(0,constants["population_size"])

		for i in range(nE):
			if (nPerPos[i] > 0):
				ax = plt.subplot2grid((5,nE),(1,i),rowspan=2)
			
				if have_seaborn:
					sns.violinplot(data[i],ax=ax)
				else:
					data[i].boxplot(ax=ax)
			
				ax.set_ylim(-2,2)

				ax1 = plt.subplot2grid((5,nE),(3,i),rowspan=2)
				t0 = np.arange(0,constants["L"]*constants["generations"])
				ax1.plot(t0,np.array(list(map(env[i].evaluate,t0)))[:,0],color=palette[i])
				ax1.scatter(t,env[i].evaluate(t)[0],s=250,color=palette[i],marker='*')
				ax1.set_ylim(-2,2)
				scale = 5*constants["L"]*env[i].R
				ax1.set_xlim(max(t0[0],t-scale/2),min(t0[-1],max(t+scale/2,scale)))

		plt.suptitle("The situation at $t = $"+str(t),fontsize=25)
		plt.subplots_adjust(top=0.95)
		#plt.tight_layout()
		plt.savefig(path+'timeseries/pop'+str(k+1)+'_genes_'+str(j)+'.png')
		plt.close()

	return mean, std



def plot_size(path,fi,k):
	nE = 0
	f = open(fi)
	for (i,row) in enumerate(f):
		if row[0]=="n":
			nE = int((i-1)/2)
			data = np.genfromtxt(fi,skiprows=i+1,delimiter=",")
			break

	sizes = data[:,-1].reshape(-1,nE)

	plt.figure()
	for i in range(nE):
		plt.plot(sizes[:,i],alpha=0.7,label="Environment "+str(i+1))
		plt.legend()
		plt.ylim(0,5000)
	plt.savefig(path+"sizes_"+str(k+1)+".png",bbox_inches='tight')
	plt.close()