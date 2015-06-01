#
# Import packages
#

import numpy as np # For efficient array operations
import matplotlib.pyplot as plt # For plotting

try: # Seaborn makes prettier plots, but is not installed in a fresh Anaconda python
	import seaborn as sns 
	have_seaborn = True
except ImportError:
	have_seaborn = False


def plot_size(path)
	nE = 0
	f = open(path)
	for (i,row) in enumerate(f):
		if row[0]=="n":
			nE = int((i-1)/2)
			data = np.genfromtxt(path,skiprows=i+1,delimiter=",")
			break

	sizes = data[:,-1].reshape(-1,nE)

	for i in range(nE):
		plt.plot(sizes[:,i],alpha=0.7,label="Environment "+str(i+1))
		plt.legend()
		plt.ylim(0,5000)
		plt.savefig("sizes.png")