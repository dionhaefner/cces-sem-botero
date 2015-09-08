#########################################################
#   output_population.py
#   Author: Dion Häfner (dionhaefner@web.de)
#   
#   Responsible for output and plotting
#   
#   Licensed under BSD 2-Clause License
#########################################################


# Import third-party libraries
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
from copy import copy
import warnings

# Seaborn makes prettier plots, but is not installed in a fresh Anaconda python
try: 
    import seaborn as sns 
    have_seaborn = True
except ImportError:
    have_seaborn = False

# Import other parts of the project
from animal import Animal
from population import Population
from environment import Environment
from constants import model_constants


def output_population(population,f1,f2,j,k,path,timeseries,t,env):
# Outputs state of the Population. Inputs:
# population: instance of Population to be output, 
# f1: file handle for mean gene file, f2: file handle for standard dev. of genes
# j: current generation counter, k: current population counter,
# path: output path, timeseries: whether complex output should be saved,
# t: current time step, env: list of environments
    constants = model_constants
    animals = np.array(population.animals())
    positions = np.array(list(map(lambda x: x.position, animals)))

    nE = len(constants["environments"])
    genes = [list(map(lambda x: x.gene_dict, animals[positions==i])) for i in range(nE)]
    nPerPos = np.array([len(genes[i]) for i in range(nE)])
    data = [pd.DataFrame(genes[i]) for i in range(nE)]
    mean = [pd.DataFrame(data[i].mean()).transpose() for i in range(nE)]
    std = [pd.DataFrame(data[i].std()).transpose() for i in range(nE)]


    for i in range(nE):
        f1.write(str(j)+","+str(i+1)+",")
        f2.write(str(j)+","+str(i+1)+",")

        if nPerPos[i] == 0:
            f1.write("0,0,0,0,0,0,0,0,0")
            f2.write("0,0,0,0,0,0,0,0,0")
        else:
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
            if (len(names) != nE):
                warnings.warn("Environment parameter and name arrays have different lengths!\
                    Disregarding names.")
                names = ["Environment "+str(q) for q in np.arange(nE)+1]
            foo = pd.DataFrame({'env': names, 'val': nPerPos})
            sns.barplot('env','val',data=foo,ax=ax,palette=palette,order=names)
        else:
            ax.bar(np.array(constants["environment_names"]),nPerPos,0.7)
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.set_ylim(0,constants["population_size"])

        for i in range(nE):
            if (nPerPos[i] > 0):
                ax = plt.subplot2grid((5,nE),(1,i),rowspan=2)
            
                if have_seaborn:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        sns.violinplot(data[i],ax=ax)
                else:
                    data[i].boxplot(ax=ax)
            
                ax.set_ylim(-2,2)

                ax1 = plt.subplot2grid((5,nE),(3,i),rowspan=2)
                scale = 5*constants["L"]*env[i].R
                if t <= constants["L"]*constants["generations"]:
                    t0 = np.arange(max(0,t-scale/2),min(constants["L"]*constants["generations"],max(t+scale/2,scale)))
                else:
                    t0 = np.arange(t-scale/2,t+scale/2)
                ax1.plot(t0,np.array(list(map(env[i].evaluate,t0)))[:,0],color=palette[i])
                ax1.scatter(t,env[i].evaluate(t)[0],s=250,color=palette[i],marker='*')
                ax1.set_ylim(-2,2)
                ax1.set_xlim(t0[0],t0[-1])


        plt.suptitle("The situation at $t = $"+str(t),fontsize=25)
        plt.subplots_adjust(top=0.95)
        plt.savefig(path+'timeseries/pop'+str(k+1)+'_genes_'+str(j)+'.png')
        plt.close()

    return mean, std



def plot_size(path,fi,k):
    constants = model_constants
    nE = 0
    f = open(fi)
    for (i,row) in enumerate(f):
        if i == 0:
            nE = int(row)
        if row[0]=="n":
            data = np.genfromtxt(fi,skiprows=i+1,delimiter=",")
            break

    sizes = data[:,-1].reshape(-1,nE)

    plt.figure()
    for i in range(nE):
        plt.plot(sizes[:,i],alpha=0.7,label="Environment "+str(i+1))
        plt.legend()
        plt.ylim(0,5000)
    plt.savefig(str(path)+"sizes_"+str(int(k)+1)+".png",bbox_inches='tight')
    plt.close()
