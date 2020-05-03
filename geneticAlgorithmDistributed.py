import random
import numpy
import time
import geneticTasks
from geneticTasks import get_fitness_scores, mating, get_best_fitness
from matplotlib import pyplot as plt
from utilityFunctions import Individual, City


def create_gene_pool():
    """
    Create a fixed amount of genes that one individual can have
    Assigns random coordinates to each city created
    """
    genes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '[', 
            ']', '{', '}', '|', ';', '<', '>', '/', '?']
    gene_pool = {}
    for gene in genes:
        gene_pool[gene] = City(random.randint(0, 30), random.randint(0, 30))

    return gene_pool    
    

class Population:
    """
    Creates a population from a gene pool and specified size or from a gene pool and a list of individuals
    Gets fitness scores and calculates the individuals with the best fitness scores
    Can make the individuals with the best fitness scores mate and produce children individuals
    """
    def __init__(self, gene_pool=None, size_of_population=10, individuals=None):
        self.gene_pool = gene_pool
        if individuals:
            self.individuals = individuals
            self.size_of_population = len(self.individuals)
        else:
            self.size_of_population = size_of_population
            self.individuals = [Individual(gene_pool=self.gene_pool) for _ in range(self.size_of_population)]
            

    def get_population(self):
        return self.individuals


    def get_fitness_scores(self): # Distributed
        """
        Return a dictionary of individuals and fitness scores
        """
        fitness = {}
        results = ~get_fitness_scores.map(self.get_population())
        for i in range(len(results)):
            fitness[self.individuals[i]] = results[i]
            
        return fitness


    def get_best_fitness_individuals(self):
        """
        Return the half of individuals with the best fitness scores
        """
        fitness_scores = self.get_fitness_scores()

        # print('getting best individuals')
        # best_individuals = get_best_fitness.apply_async((fitness_scores,), serializer='pickle')
        # print(best_individuals)
        best_individuals = []

        halve_population = len(fitness_scores) // 2 
        if halve_population % 2 == 1:  # Need to make the half of the population even in order for everyone to be able to mate
            halve_population -= 1

        for _ in range(halve_population):
            for individual, score in fitness_scores.items():
                if score == min(fitness_scores.values()):
                    best_individuals.append(individual)
                    fitness_scores[individual] = max(fitness_scores.values())
                    break
        # best_individuals = [Individual(gene_pool=self.gene_pool, gene_sequence=individual_genes) for individual_genes in best_individuals]

        return best_individuals


    def mate(self):  # Distributed
        """
        Gets the best individuals from the population 
        Takes a random subset of the second parents gene sequence and copies it directly into a copy of the 
        first parents gene sequence at the same positions. This is the new child gene sequence
        Creates a new individual instance for every child
        """
        best_individuals = self.get_best_fitness_individuals()

        children = mating.apply_async(args=(best_individuals, self.gene_pool)).get()

        best_individuals += [Individual(gene_pool=self.gene_pool, gene_sequence=child_genes) for child_genes in children]

        return best_individuals


def create_plot(generations, fitness_counts):
    """
    Graphs the average fitness score for every generation
    """
    print(generations)
    print('fitness counts', fitness_counts)
    plt.plot(generations, fitness_counts, color='lightblue', linewidth=3)
    plt.title('Fitness Score per Generation')
    plt.xlabel('Generation')
    plt.ylabel('Fitness Score')
    plt.grid(True)
    plt.show()


def average_fitnesses(individuals):  # Distributed
    """
    Calculate the average fitness score for a generation of individuals
    """
    all_fitness_scores = ~get_fitness_scores.map(individuals)
    return sum(all_fitness_scores) / len(individuals)


def main():
    start = time.monotonic()
    # Create gene pool and beginning population
    gene_pool = create_gene_pool()
    population = Population(gene_pool=gene_pool, size_of_population=1000)  # Split size of population into multiple parts and then join together into one population
    # creates all individuals and puts it into list
    generation = []
    fitness_counts = []

    generation_count = 0
    while population.size_of_population > 1:
        # Get all the individuals in the population
        generation.append(generation_count)
        individuals = population.get_population()
        
        # Calculate the average for the population in order to graph later
        fitness_counts.append(average_fitnesses(individuals))

        # Create the new population as the children after mating the best half of the population
        children = population.mate()

        if len(children) == 0:
            break

        population = Population(gene_pool=gene_pool, individuals=children)

        # Increment generation
        generation_count += 1

    print(time.monotonic() - start)
    # Plot the average fitness score per generation
    create_plot(generation, fitness_counts)    


if __name__ == '__main__':
    main()
