#!/usr/bin/env python

#########################################################
#	botero.py
#	Author: Dion Häfner (dionhaefner@web.de)
#	
#	Convenience module for executing the project, based
#	on command-line user-input.
#
#	Licensed under BSD 2-Clause License
#########################################################

import sys
sys.path.insert(0, './src')

import main_constant
import main_variable

####
# User input for each variable. Every query is repeated until valid input is given.
####

print("\nWelcome to the population simulation programme based on the work of Botero et al.!")
print("You will now be asked some questions. You can abort the programme by hitting ctrl-c in most shells.\n")
model = ""
while model not in ["1","0"]:
	model = input("Run simulation with constant (1) or variable (0) population size? ")

valid = False
while not valid:
	populations = input("How many similar populations should be simulated? ")
	try:
		if int(populations) > 0:
			valid = True
	except (TypeError,ValueError):
		pass


if model == "1": # constant population size
	valid = False
	while not valid:
		R = input("Which environment time scale? ")
		try:
			if float(R) > 0:
				valid = True
		except (TypeError,ValueError):
			pass

	timeseries = ""
	while timeseries not in ["y","n"]:
		timeseries = input("Detailed output after every time step? (y/n) ")
	if timeseries == "y":
		timeseries = True
	else:
		timeseries = False

	main_constant.main(int(populations), float(R), timeseries)


else: # variable population size
	valid = False
	while not valid:
		f_mean = input("Specify path to the mean gene file: ")
		try:
			f = open(f_mean)
			if f:
				valid = True
		except (IOError,FileNotFoundError):
			print("File does not exist or cannot be opened! ")
			pass

	valid = False
	while not valid:
		f_std = input("Specify path to the std. dev. gene file: ")
		try:
			f = open(f_std)
			if f:
				valid = True
		except (IOError,FileNotFoundError):
			print("File does not exist or cannot be opened! ")
			pass

	valid = False
	while not valid:
		nR = input("Which new environment time scale? ")
		try:
			if float(nR) > 0:
				valid = True
		except (TypeError,ValueError):
			pass

	valid = False
	while not valid:
		nP = input("Which new environment predictability? ")
		try:
			if float(nP) > 0:
				valid = True
		except (TypeError,ValueError):
			pass

	timeseries = ""
	while timeseries not in ["y","n"]:
		timeseries = input("Detailed output after every time step? (y/n) ")
	if timeseries == "y":
		timeseries = True
	else:
		timeseries = False

	main_variable.main(f_mean,f_std,float(nR),float(nP),int(populations),timeseries)