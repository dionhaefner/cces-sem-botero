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
from iterate_population_var import iterate_population_var # Main controller for population iteration





# Get model constants
constants = model_constants()

# Get parameters from command line
arguments = sys.argv[1:]
if (len(arguments) !=14 ):
    print("Usage: main.py [population] [R] [P] [A] [B] [year] [month] [day] [HH] [MM] [SS] [nR] [nP] [n]")
    print("E.g. $ python main_var.py 5 1 0 1 0 15 05 08 10 44 05 10 1")
    sys.exit(0)
else:
    try:
        n_pop = int(arguments[0])
        R, P, A, B = list(map(float,arguments[1:5]))
        year = arguments[5]
        month = arguments[6]
        day = arguments[7]
        hour = arguments[8]
        minute = arguments[9]
        sec = arguments[10]
        nR = float(arguments[11])
        nP = float(arguments[12])
        populations = int(arguments[13])
            
    except ValueError:
        print("Usage: main.py [population] [R] [P] [A] [B] [year] [month] [day] [HH] [MM] [SS] [nR] [nP] [n]")
        print("E.g. $ python main_var.py 5 1 0 1 0 15 05 08 10 44 05 10 1\n")
        raise

path0 = "./output/R{0}-P{1}-A{2}-B{3}_{4}-{5}-{6}_{7}-{8}-{9}/".format(R,P,A,B,year,month,day,hour,minute,sec)
# create output directory
now = datetime.datetime.today()
path = "./output_var/R{0}-P{1}-A{2}-B{3}_{4:%y}-{4:%m}-{4:%d}_{4:%H}-{4:%M}-{4:%S}/".format(R,P,A,B,now)
try: 
	os.makedirs(path)
	os.makedirs(path+"timeseries/")
except OSError:
	if not os.path.isdir(path):
		raise

start = time.clock()

# read the csv file
n = str(n_pop)
import csv
with open(path0+'pop'+n+'_mean_genes.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        #print(row)
        lst = row
    
# only use the mean genes of the last generation     
num = [float(i) for i in lst]

with open(path0+'pop'+n+'_std_genes.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        #print(row)
        lst = row
num_std = [float(i) for i in lst]
num_std = np.fabs(num_std)

f3 = open(path+"pop"+n+"__overview.csv",'w')
f3.write("initial conditions \n")
f3.write("R,P,A,B\n{0},{1},{2},{3}\nn,I0,I0p,a,b,bp,h,s\n".format(R,P,A,B))
f3.write("{0},{1},{2},{3},{4},{5},{6},{7}\n".format(n_pop,num[1],num[2],num[3],num[4],num[5],num[6],num[7]))
f3.write("{0},{1},{2},{3},{4},{5},{6},{7}\n".format(n_pop,num_std[1],num_std[2],num_std[3],num_std[4],num_std[5],num_std[6],num_std[7]))
f3.write("mu = {0}".format(constants["mu"]))
f3.write("\n\n")

survival_rate = 0

for k in range(populations):
    # write starting genes in files
    f1 = open(path+"pop"+str(k+1)+"_mean_genes.csv",'w')
    f1.write("initial conditions \n")
    f1.write("R,P,A,B\n{0},{1},{2},{3}\nn,I0,I0p,a,b,bp,h,s\n".format(R,P,A,B))
    f1.write("{0},{1},{2},{3},{4},{5},{6},{7}\n".format(n_pop,num[1],num[2],num[3],num[4],num[5],num[6],num[7]))
    f1.write("\n\n")
    
    f2 = open(path+"pop"+str(k+1)+"_std_genes.csv",'w')
    f2.write("initial conditions \n")
    f2.write("R,P,A,B\n{0},{1},{2},{3}\nn,I0,I0p,a,b,bp,h,s\n".format(R,P,A,B))
    f2.write("{0},{1},{2},{3},{4},{5},{6},{7}\n".format(n_pop,num[1],num[2],num[3],num[4],num[5],num[6],num[7]))
    f2.write("\n\n")
        
    # create genome with the mean genes that shall be tested
    genes = []
    for l in range(constants["population_size"]):
        h = np.random.normal(loc=num[6],scale=num_std[6])
        s = np.random.normal(loc=num[7],scale=num_std[7])
        
        if (num_std[3] == 0):
            a = num[3]
        else:
            a = np.random.normal(loc=num[3],scale=num_std[3])
            
        I0 = np.random.normal(loc=num[1],scale=num_std[1])
        I0p = np.random.normal(loc=num[2],scale=num_std[2])
        
        if (num_std[4] == 0):
            b = num[4]
        else:
            b = np.random.normal(loc=num[4],scale=num_std[4])
            
        if (num_std[5] == 0):
            bp = num[5]
        else:
            bp = np.random.normal(loc=num[5],scale=num_std[5])
        #genes.append(Genome([num[6],num[7],num[3],num[1],num[2],num[4],num[5]]))
        genes.append(Genome([h,s,a,I0,I0p,b,bp]))
        
    # create a population of population_size animals that already
    # have the correct mean genes
    animal_list = [Animal(genes[x]) for x in range(constants["population_size"])]
    population = Population(constants["population_size"],animal_list)
    
    end = time.clock()
    print("Set-up time: {0}\n".format(end-start))
    start = time.clock()
    
    f3.write("Population {0}".format(k+1))
    pop_mean, pop_std, stop = iterate_population_var(k,population,nR,nP,A,B,path,0,f1,f2,f3)
    if (stop == 0):
        survival_rate = survival_rate+1
        f3.write(" survived!")
    end = time.clock()
    print("\n---------------------------------------")
    print(" Population {0} done! Total time: {1:.2f} min".format(k+1,(end-start)/60))
    print("---------------------------------------\n")

f3.write("\n\nIn total {0}/{1} Populations survived.".format(survival_rate,populations))