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

try:
    input_delay = input("Delay between iterations (seconds)? Press Enter for no delay, or enter a number: ")
    iteration_delay = float(input_delay) if input_delay else 0
except:
    print("Invalid value - Using no delay")
    iteration_delay = 0

input_visual = input("Show visual board for each iteration? (yes/no, press Enter for no): ").lower()
show_visual = input_visual == 'yes'

input_elite = input("Use elitism? (yes/no, press Enter for yes): ").lower()
use_elitism = input_elite != 'no'

input_tournament = input("Tournament selection size (2-10, press Enter for 3): ")
tournament_size = int(input_tournament) if input_tournament.isdigit() and 2 <= int(input_tournament) <= 10 else 3

input_adaptive = input("Use adaptive mutation? (yes/no, press Enter for yes): ").lower()
adaptive_mutation = input_adaptive != 'no'

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


def print_board(chromosome):
    """Prints a visual representation of the chess board"""
    print("\n  " + "-" * (queens * 2 + 1))
    for i in range(queens):
        row = "| "
        for j in range(queens):
            row += "Q " if chromosome[j] == i else ". "
        print(row + "|")
    print("  " + "-" * (queens * 2 + 1))

def tournament_selection():
    """Tournament selection for better parent selection"""
    tournament = np.random.choice(population, tournament_size, replace=False)
    return max(tournament, key=lambda x: x.fitness)

def adaptiveMutationRate(best_fitness):
    # Adjusts mutation rate based on population fitness
    if adaptive_mutation:
        return mutationValue * (1 - (best_fitness / maximumFitness))
    return mutationValue

def getParents():
    if tournament_size > 0:
        parent1 = tournament_selection()
        parent2 = tournament_selection()
        while parent2 == parent1:
            parent2 = tournament_selection()
        return parent1, parent2, np.sum([x.fitness for x in population])
    
    # Original parent selection logic (roulette wheel selection)
    total_fitness = np.sum([x.fitness for x in population])
    probabilities = [x.fitness/total_fitness for x in population]
    
    parent1 = np.random.choice(population, p=probabilities)
    parent2 = np.random.choice(population, p=probabilities)
    while parent2 == parent1:
        parent2 = np.random.choice(population, p=probabilities)
    
    return parent1, parent2, total_fitness

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

# According to genetic theory, mutation occurs when an abnormality occurs terminating the crossover situation.
# Since a computer cannot detect such an anomaly, we can identify the probability of developing such a mutation ourselves.

	if child.survival != None:
		if child.survival < mutationValue:
			c = np.random.randint(8)
			child.order[c] = np.random.randint(8)
	return child

def geneticAlgorithm(iteration):
    print(f"\n{'='*20} Generation #{iteration} {'='*20}")
    
    # Calculate current best fitness
    current_best = max(population, key=lambda x: x.fitness)
    print(f"Current Best Fitness: {current_best.fitness}/{maximumFitness}")
    
    if show_visual:
        print_board(current_best.order)
    
    newPopulation = []
    
    # Elitism: Keep the best individual
    if use_elitism:
        newPopulation.append(current_best)
    
    # Generate new population
    while len(newPopulation) < len(population):
        parent1, parent2, sum_fit = getParents()
        
        if crossoverType == 1:
            child = singlePoint_crossover(parent1, parent2)
        else:
            child = twoPoint_crossover(parent1, parent2)
        
        # Adaptive mutation
        current_mutation_rate = adaptiveMutationRate(current_best.fitness)
        if mutationParams and np.random.random() < current_mutation_rate:
            child = mutate(child)
        
        newPopulation.append(child)
    
    # Add delay if specified
    if iteration_delay > 0:
        time.sleep(iteration_delay)
    
    return newPopulation

def terminate():
    fitnessvals = [pos.fitness for pos in population]
    max_value = np.max(fitnessvals)
    avg_value = np.mean(fitnessvals)
    
    print(f"\nGeneration Statistics:")
    print(f"Best Fitness: {max_value}/{maximumFitness}")
    print(f"Average Fitness: {avg_value:.2f}")
    print(f"Current Mutation Rate: {adaptiveMutationRate(max_value):.4f}")
    print("_" * 50)
    
    if maximumFitness in fitnessvals:
        print("\n*** Solution Found! ***")
        beep()
        return True
    if maximumIteration == iteration:
        print("\n*** Maximum iterations reached! ***")
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

input("Press Enter key to exit...")
