from constants import model_constants
from popclasses import *
from environment import *
import sys

# Get parameters from command line
arguments = sys.argv[1:]
if (len(arguments) !=11 ):
    print("Usage: main.py [populations] [R] [P] [A] [B] [year] [month] [day] [HH] [MM] [SS]")
    print("E.g. $ python fitness.py 100 1 0 1 0 15 05 08 10 44 05")
    sys.exit(0)
else:
    try:
        populations = int(arguments[0])
        R, P, A, B = list(map(float,arguments[1:5]))
        year = arguments[5]
        month = arguments[6]
        day = arguments[7]
        hour = arguments[8]
        minute = arguments[9]
        sec = arguments[10]
            
    except ValueError:
        print("Usage: main.py [populations] [R] [P] [A] [B] [year] [month] [day] [HH] [MM] [SS]")
        print("E.g. $ python fitness.py 100 1 0 1 0 15 05 08 10 44 05 \n")
        raise

path = "./output/R{0}-P{1}-A{2}-B{3}_{4}-{5}-{6}_{7}-{8}-{9}/".format(R,P,A,B,year,month,day,hour,minute,sec)

f1 = open(path+"fitness.csv",'w')
f1.write("R,P,A,B\n{0},{1},{2},{3}\n\n".format(R,P,A,B))
f1.write("nPop, Mean Payoff, Mean Payoff for each lifetime\n")

# loop over all populations
for n_pop in range(populations):
    
    # read the csv file
    n = str(n_pop+1)
    import csv
    with open(path+'pop'+n+'_mean_genes.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            #print(row)
            lst = row
    
    # only use the mean genes of the last generation     
    num = [float(i) for i in lst]
    
    # create genome with the mean genes that shall be tested
    genes = Genome([num[1],num[2],num[3],num[4],num[5],num[6],num[7]])
    
    # create a population of population_size animals that already have the correct mean genes
    # full population size is chosen to see if DBH is a good strategy
    animal_list = [Animal(genes) for _ in range(constants["population_size"])]
    
    # loop over R to represent a full environmental cycle
    gen_payoff = []
    r = int(R)
    for _ in range(r):
        
        # create a Population from animal_list
        population = Population(constants["population_size"],animal_list)
        
        # let the Population live for one generation without breeding
        t = 0
        E, C = environment(t,R,P,A,B)
        population.react(E,C,1)
        t = t+1
        
        for _ in range(constants["L"]):
        
        	E, C = environment(t,R,P,A,B)
        	population.react(E,C)
        	t = t+1
         
        payoff = []
        # calculate the lifetime payoff of each animal
        for animal in population.animals():
            payoff.append(population._lifetime_payoff(animal))
        
        gen_payoff.append(np.mean(payoff)) 
        
    #print(gen_payoff)
    mean_payoff = np.mean(gen_payoff)
    print(mean_payoff)
        
    f1.write("{0}, {1}, {2}\n".format(n_pop,mean_payoff,gen_payoff))
