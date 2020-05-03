import time
from geneticTasks import get_fitness_scores, mating, get_best_fitness
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


    def get_best_fitness_individuals(self):  # Distributed
        """
        Return the half of individuals with the best fitness scores
        """
        individuals_and_fitness = self.get_fitness_scores()

        # Obtain the gene sequences of the best individuals
        best_individuals, extra_population = get_best_fitness.apply_async((individuals_and_fitness,)).get()  
        
        # Create Individuals from the obtained gene sequences
        best_individuals = [Individual(gene_pool=self.get_gene_pool(), gene_sequence=individual_genes) for individual_genes in best_individuals]
        extra_population = [Individual(gene_pool=self.get_gene_pool(), gene_sequence=individual_genes) for individual_genes in extra_population]

        return best_individuals, extra_population


    def mate(self):  # Distributed
        """
        Gets the best individuals from the population 
        Takes a random subset of the second parents gene sequence and copies it directly into a copy of the 
        first parents gene sequence at the same positions. This is the new child gene sequence
        Creates a new individual instance for every child
        """
        best_individuals, extra_individuals = self.get_best_fitness_individuals()


        # Mate the best individuals and receive a list of child gene sequences
        children = mating.apply_async((best_individuals, self.get_gene_pool())).get()

        # Create a list of individuals from the list of child gene sequences
        best_individuals += [Individual(gene_pool=self.gene_pool, gene_sequence=child_genes) for child_genes in children] + extra_individuals
    
        return best_individuals


def average_fitnesses(individuals):  # Distributed
    """
    Calculate the average fitness score for a generation of individuals
    """
    all_fitness_scores = ~get_fitness_scores.map(individuals)
    return sum(all_fitness_scores) / len(individuals)


def main():
    AMOUNT_OF_GENERATIONS = 5000
    SIZE_OF_POPULATION = 1000

    start = time.monotonic()
    # Create gene pool and beginning population
    gene_pool = create_gene_pool()
    population = Generation(gene_pool=gene_pool, size_of_population=SIZE_OF_POPULATION)
    # creates all individuals and puts it into list
    generation = []
    fitness_counts = []

    generation_count = 0
    while generation_count <= AMOUNT_OF_GENERATIONS:
        # Get all the individuals in the population
        generation.append(generation_count)
        individuals = population.get_population()
        
        # Calculate the average for the population in order to graph later
        fitness_counts.append(average_fitnesses(individuals))

        # Create the new population as the children after mating the best half of the population
        children = population.mate()

        if len(children) == 0:
            break

        population = Generation(gene_pool=gene_pool, individuals=children)

        # Increment generation
        generation_count += 1

    print(time.monotonic() - start)
    # Plot the average fitness score per generation
    create_plot(generation, fitness_counts)    


if __name__ == '__main__':
    main()
