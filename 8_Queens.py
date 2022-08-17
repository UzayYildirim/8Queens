# Import libraries

import numpy as np
import time

# Uzay Yıldırım

print("")
print("")
print("   ___       ____                                      ")
print("  / _ \     / __ \                                     ")
print(" | (_) |   | |  | |  _   _    ___    ___   _ __    ___ ")
print("  > _ <    | |  | | | | | |  / _ \  / _ \ | '_ \  / __|")
print(" | (_) |   | |__| | | |_| | |  __/ |  __/ | | | | \__ \ ")
print("  \___/     \___\_\  \__,_|  \___|  \___| |_| |_| |___/")
print("")
print("")
print("[+][+][+][+][+][+][+][+][+][+]")
print("")

# Startup

queens = 0

# User settings
try:
	queensInput = int(input("What size should the board be? Possible values: 8 / 16 / 32 (Recommended: 8) |"))
	if queensInput == 8:
		queens = 8
	elif queensInput == 16:
		queens = 16
	elif queensInput == 32:
		print("You have selected 32 - Only up to n=26 results have been found yet. The process can take centuries to complete.")
		queens = 32
	else:
		print("Invalid value - Using the default value. (8)")
		queens = 8
except:
    print("Invalid value - Using the default value. (8)")
    queens = 8

input_crossoverType = str(input("Crossover Type (Single Point/Double Point) Possible values: 1 / 2 (Recommended: 1) | "))
if input_crossoverType == "1":
    crossoverType = 1
elif input_crossoverType == "2":
    crossoverType = 2
else:
    print("Invalid value - Using the default value. (1 **Single Point**)")
    crossoverType = 1
input_mutation = str(input("Use mutation? Possible values: yes / no (Recommended: yes) | "))
if input_mutation == "yes":
    mutationParams = True
elif input_mutation == "no":
    mutationParams = False
else:
    print("Invalid value - Using the default value. (Use mutation)")
    mutationParams = True
    
try:
    input_maxIterations = int(input("How many iterations can be done? (Recommended: 2000) | "))
except:
    print("Invalid value - Using the default value. (2000 Maximum Iterations)")
    input_maxIterations = 2000

populationCount = queens * 150 # The population number is calculated according to user's given parameters.
maximumFitness = (queens * (queens - 1)) / 2 # Maximum possible Fitness value. (28 for 8 Queens)
mutationValue = 0.005 # The value to base the mutation on.
maximumIteration = input_maxIterations 
population = None

print("[+][+][+][+][+][+][+]")
print("[+] STARTING UP [+]")
print("[+][+][+][+][+][+][+]")

class board:
	def __init__(self):
		self.order = None
		self.fitness = None
		self.survival = None
	def setorder(self, val):
		self.order = val
	def setFitness(self, fitness):
		self.fitness = fitness
	def setSurvival(self, val):
		self.survival = val

def fitness(chromosome = None):
	conflict = 0
	row_col_conflict = abs(len(chromosome) - len(np.unique(chromosome)))
	conflict += row_col_conflict

	for i in range(len(chromosome)):
		for j in range(len(chromosome)):
			if ( i != j):
				dx = abs(i-j)
				dy = abs(chromosome[i] - chromosome[j])
				if(dx == dy):
					conflict += 1
	return maximumFitness - conflict	

def createChromosome():
	global queens
	init_distribution = np.arange(queens)
	np.random.shuffle(init_distribution)
	return init_distribution

def createPopulation(populationSize = 100):
	global population
	print ("> Creating the first generation...")
	while True:
		population = populationSize
		population = [board() for i in range(populationSize)]
		for i in range(populationSize):
			population[i].setorder(createChromosome())
			population[i].setFitness(fitness(population[i].order))

		fitnessvals = [pos.fitness for pos in population]
		maxfitnessvar = (maximumFitness in fitnessvals) 
		if maxfitnessvar == False:
			break
	return population


def getParents():	
	parent1, parent2 = None, None
    
	# Parents are randomly selected based on probability of survival.
	# To find the solution we need to normalize the Fitness value.
	
	sum_fitness = np.sum([x.fitness for x in population])
	for each in population:
		each.survival = each.fitness/(sum_fitness*1.0)

	while True:
		parent1_random = np.random.rand()
		parent1_rn = [x for x in population if x.survival <= parent1_random]
		try:
			t = np.random.randint(len(parent1_rn))
			parent1 = parent1_rn[t]
			break
		except:
			pass

	while True:
		parent2_random = np.random.rand()
		parent2_rn = [x for x in population if x.survival <= parent2_random]
		try:
			t = np.random.randint(len(parent2_rn))
			parent2 = parent2_rn[t]
			if parent2 != parent1:
				break
			else:
				print ("< ! > Equal parents, re-iterating...")
				continue
		except:
			continue

	if parent1 is not None and parent2 is not None:
		return parent1, parent2, sum_fitness

def singlePoint_crossover(parent1, parent2): # Single-Point Crossover
	n = len(parent1.order)
	c = np.random.randint(n, size=1)
	cp = int(c)
	child = board()
	child.order = []
	child.order.extend(parent1.order[0:cp])
	child.order.extend(parent2.order[cp:])
	child.setFitness(fitness(child.order))	
	return child

def twoPoint_crossover(parent1, parent2): # Two-Point Crossover
	n = len(parent1.order)
	c1 = np.random.randint(0, n / 2, size=1)
	cp = int(c1)
	c2 = np.random.randint((n / 2) + 1, n, size=1)
	cp2 = int(c2)
	child = board()
	child.order = []
	child.order.extend(parent1.order[0:cp])
	child.order.extend(parent2.order[cp:cp2])
	child.order.extend(parent1.order[cp2:])
	child.setFitness(fitness(child.order))	
	return child

def mutate(child):
	"""	
	- According to genetic theory, mutation occurs when an abnormality occurs terminateing the crossover situation.
	- Since a computer cannot detect such an anomaly, we can identify the probability of developing such a mutation ourselves.
	"""
	if child.survival != None:
		if child.survival < mutationValue:
			c = np.random.randint(8)
			child.order[c] = np.random.randint(8)
	return child

def geneticAlgorithm(iteration):
	print ("[+] [+] [+] [+] " ,"Genetic Generation: >> #", int(iteration), " [+] [+] [+] [+] ")
	newPopulation = []
	for i in range(len(population)):
		parent1, parent2, sum_fit = getParents()
		# print ("Produced parents: ", parent1, parent2)
		if crossoverType == "1":
			child = singlePoint_crossover(parent1, parent2)
		else:
			child = twoPoint_crossover(parent1, parent2)
		sum_fit += child.fitness
		child.survival = child.fitness/(sum_fit*1.0)
		if(mutationParams):
			child = mutate(child)

		newPopulation.append(child)
	return newPopulation

def terminate():
	fitnessvals = [pos.fitness for pos in population]
	max_value = np.max(fitnessvals)
	print ("> Best Fitness value of this generation: ", max_value, " / ", maximumFitness)
	print("________________________________________________________________________")
	if maximumFitness in fitnessvals:
		print("Done!")
		beep()
		return True
	if maximumIteration == iteration:
		print("The maximum number of iterations has been reached. Timeout.")
		return True
	return False

def beep():
	print ("\a")

population = createPopulation(populationCount)
i = 1
print ("Population size: ", len(population))

iteration = 0;
while not terminate():
	# Continue iterating until the best position is found.
	population = geneticAlgorithm(iteration)
	iteration +=1 

print (f"A total of {iteration} iterations has been made.")
for each in population:
	if each.fitness == maximumFitness:
		print (each.order)

time.sleep(4)

input("Press Enter key to exit 8 Queens...")