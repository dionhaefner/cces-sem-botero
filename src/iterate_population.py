#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
#########################################################
#
#   iterate_population.py
#   Author: Dion Häfner (dionhaefner@web.de)
#   
#   Main controller for a given population
#   
#   Licensed under BSD 2-Clause License
#
#########################################################
"""

# Import third party libraries
import numpy as np 
import time
import sys

# Import other parts of the project
from animal import Animal
from population import Population
from environment import Environment
from constants import model_constants
from output_population import output_population, plot_size


def iterate_population(k,population,environments,f1,f2,path,t=0,variable=False):
    """ 
    MAIN CONTROLLER
    Inputs:
        k: population counter,  population: the Population instance to be iterated,
        environments: Environment instances to be operated on,
        f1: pointer to output file for gene means,  f2: for gene standard deviations,
        path: path to the output files  t: initial time,   
        variable: variable population size
    """

    constants = model_constants
    nE = len(environments)

    for j in np.arange(constants["generations"]):
        # MAIN TIME STEP LOOP
        start = time.clock()

        output_population(population,f1,f2,j,k,path,False,t,environments)

        for _ in range(constants["L"]):
            E, C = np.empty(nE), np.empty(nE)

            for (i,env) in enumerate(environments):
                E[i], C[i] = env.evaluate(t)

            population.react(E,C)
            t = t+1

        if variable:
            population.breed_variable()
        else:
            population.breed_constant()

        if population.size() == 0:
            print("Population died out!\n\n")
            return None, None, j

        population.react(E,C,1)

        end = time.clock()
        if constants["verbose"]:
            print("Computation time: {0:.2e}s".format(end-start))

	    # Print progress bar
        percent = float(j+1) / constants["generations"]
        hashes = '#' * int(round(percent * 20))
        spaces = ' ' * (20 - len(hashes))
        sys.stdout.write("\rProgress population {2} of {3}: [{0}] {1:.1f}%".format(hashes + spaces, percent * 100,k+1,constants["populations"]))
        sys.stdout.flush()


    # Final outputs for each population
    final_mean, final_std = output_population(population,f1,f2,j,k,path,True,t,environments)
    f1.close()
    f2.close()

    plot_size(path,path+"pop"+str(k+1)+"_mean_genes.csv",k)

    return final_mean, final_std, j
