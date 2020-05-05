import time
import random
from geneticTasks import get_fitness_scores, mating, mutation
from utilityFunctions import Individual, City, Population, create_gene_pool, create_plot


class Generation(Population):
    """
    Inherits parent class Population
    Creates a population from a gene pool and specified size or from a gene pool and a list of individuals
    Gets fitness scores and calculates the individuals with the best fitness scores
    Can make the individuals with the best fitness scores mate and produce children individuals
    """
    def __init__(self, gene_pool=None, size_of_population=10, individuals=None):
        super().__init__(gene_pool, size_of_population, individuals)


    def get_fitness_scores(self): # Distributed
        """
        Return a dictionary of individuals and fitness scores
        """
        individuals = []
        fitness_scores = []
        population = self.get_population()
        results = ~get_fitness_scores.map(population)
        for i in range(len(results)):
            individuals.append(population[i])
            fitness_scores.append(results[i])
            
        return individuals, fitness_scores


    def mate(self):  # Distributed
        """
        Gets the best individuals from the population 
        Takes a random subset of the second parents gene sequence and copies it directly into a copy of the 
        first parents gene sequence at the same positions. This is the new child gene sequence
        Creates a new individual instance for every child
        """
        best_individuals, extra_individuals = self.get_best_fitness_individuals()

        # Mate the best individuals and receive a list of child gene sequences
        children = ~mating.chunks([(best_individuals[i], best_individuals[i + 1]) for i in range(0, len(best_individuals), 2)], 10)

        # Format the the list properly
        children = children[0]

        # Create a list of individuals from the list of child gene sequences
        best_individuals += [Individual(gene_pool=self.gene_pool, gene_sequence=child_genes) for child_genes in children] + extra_individuals
    
        return best_individuals


    def mutate(self, mutation_rate):
        if random.random() < mutation_rate:
            population = self.get_population()
            ~mutation.map(population)



def average_fitnesses(individuals):  # Distributed
    """
    Calculate the average fitness score for a generation of individuals
    """
    all_fitness_scores = ~get_fitness_scores.map(individuals)
    return sum(all_fitness_scores) / len(individuals)


def main():
    AMOUNT_OF_GENERATIONS = 100
    SIZE_OF_POPULATION = 500
    MUTATION_RATE = 0.2

    start = time.monotonic()

    # Create gene pool and initial population
    gene_pool = create_gene_pool()
    population = Generation(gene_pool=gene_pool, size_of_population=SIZE_OF_POPULATION)

    generation = []
    fitness_counts = []

    generation_count = 0
    while generation_count <= AMOUNT_OF_GENERATIONS:

        generation.append(generation_count)

        # Get all the individuals in the population
        individuals = population.get_population()
        
        # Calculate the average for the population in order to graph later
        fitness_counts.append(average_fitnesses(individuals))

        print('mating')
        children = population.mate()
        print('done')

        # Create the new population as the children after mating the best half of the population and apply mutation
        population = Generation(gene_pool=gene_pool, individuals=children)
        population.mutate(MUTATION_RATE)

        # Increment generation
        generation_count += 1

    print(time.monotonic() - start)

    # Plot the average fitness score per generation
    create_plot(generation, fitness_counts)    


if __name__ == '__main__':
    main()
