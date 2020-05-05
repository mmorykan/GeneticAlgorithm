import random
import numpy
from matplotlib import pyplot as plt

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


class City:
    """
    Creates the city as a pair of x and y coordiantes.
    Can calculate the distance between two cities
    """
    def __init__(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord


    def get_distance(self, city):
        x_distance = abs(self.x_coord - city.x_coord)
        y_distance = abs(self.y_coord - city.y_coord)
        return numpy.sqrt(x_distance**2 + y_distance**2)


class Individual:
    """
    Creates an individual by creating its own gene sequence
    Calculates the fitness quality of an individual
    """
    def __init__(self, gene_pool, gene_sequence=None, fitness=None):
        self.gene_pool = gene_pool
        if gene_sequence:
            self.gene_sequence = gene_sequence
        else:
            self.gene_sequence = self.create_gene_sequence()
        if fitness:
            self.fitness = fitness
        else:
            self.fitness = self.determine_fitness()


    def create_gene_sequence(self):
        """
        Creates one individual by randomly taking a sample from the gene pool and adding the home city on the end
        """
        gene_sequence = random.sample(list(self.gene_pool), len(self.gene_pool))
        gene_sequence += gene_sequence[0]
        self.gene_sequence = gene_sequence
        return gene_sequence


    def determine_fitness(self):
        """
        Calculate the distance between each city. The total distance is the fitness value
        """
        total_distance = 0
        gene_sequence = self.get_gene_sequence()
        for gene in range(len(gene_sequence) - 1):
            city_1 = self.gene_pool[gene_sequence[gene]]
            city_2 = self.gene_pool[gene_sequence[gene + 1]]
            total_distance += city_1.get_distance(city_2)

        self.fitness = total_distance

        return total_distance


    def mutate(self):
        """
        Randomly swaps two genes in an individuals gene sequence in order to mutate
        """
        gene_sequence = self.get_gene_sequence()

        gene_to_swap = random.randint(1, len(gene_sequence) - 2)
        gene_to_swap_with = random.randint(1, len(gene_sequence) - 2)

        saved_gene = gene_sequence[gene_to_swap]
        gene_sequence[gene_to_swap] = gene_sequence[gene_to_swap_with]
        gene_sequence[gene_to_swap_with] = saved_gene


    def get_gene_sequence(self):
        return self.gene_sequence


    def get_fitness(self):
        return self.fitness

    
    def get_gene_pool(self):
        return self.gene_pool


class Population:
    """
    Creates a population from a gene pool and specified size or from a gene pool and a list of individuals
    Gets fitness scores and calculates the individuals with the best fitness scores
    Can make the individuals with the best fitness scores mate and produce children individuals
    """
    def __init__(self, gene_pool=None, size_of_population=10, individuals=None):
        self.gene_pool = gene_pool
        # If individual list is not given, create random individuals based on size of population
        if individuals:
            self.individuals = individuals
            self.size_of_population = len(self.individuals)
        else:
            self.size_of_population = size_of_population
            self.individuals = [Individual(gene_pool=self.gene_pool) for _ in range(self.size_of_population)]
            

    def get_population(self):
        return self.individuals


    def get_gene_pool(self):
        return self.gene_pool


    def get_size_of_population(self):
        return self.size_of_population


    def get_fitness_scores(self):
        """
        Return a dictionary of individuals as keys and fitness scores as values
        """
        individuals = []
        fitness_scores = []
        for individual in self.get_population():
            fitness_score = individual.get_fitness()
            individuals.append(individual)
            fitness_scores.append(fitness_score)
        
        return individuals, fitness_scores


    def get_best_fitness_individuals(self):
        """
        Return the half of individuals in the population with the best fitness scores
        """
        individuals, fitness_scores = self.get_fitness_scores()
        extra_population = []
        mating_individuals = []

        halve_population = len(fitness_scores) // 2 
        if halve_population % 2 == 1:  # Need to make the half of the population even in order for everyone to be able to mate
            halve_population -= 1


        partial_population = int(len(fitness_scores) * (3 / 4))


        for _ in range(partial_population):
            # Gets the index of the best fitness score and saves the individual with that score
            index = fitness_scores.index(min(fitness_scores))
            if _ >= halve_population:
                extra_population.append(individuals[index])
            else:
                mating_individuals.append(individuals[index])
            fitness_scores[index] = max(fitness_scores)
            # fitness_scores.pop(index)

        return mating_individuals, extra_population


    def mate(self):
        """
        Gets the best individuals from the population 
        Takes a random subset of the second parents gene sequence and copies it directly into a copy of the 
        first parents gene sequence at the same positions. This is the new child gene sequence
        Creates a new individual instance for every child
        """
        best_individuals, extra_population = self.get_best_fitness_individuals()
        children = []

        # Iterate over every pair of the best parents
        for i in range(0, len(best_individuals), 2):

            # Get two parents
            parent_1 = best_individuals[i]
            parent_2 = best_individuals[i + 1]

            # Get the two parents' gene sequences
            parent_1_gene_sequence = parent_1.get_gene_sequence()
            parent_2_gene_sequence = parent_2.get_gene_sequence()

            # Obtain a sample of the second parents gene sequence randomly
            start_gene_index = random.randint(1, len(parent_2_gene_sequence) - 2)
            end_gene_index = random.randint(start_gene_index + 1, len(parent_2_gene_sequence) - 1)

            # Get the correct genes from parent 2 
            parent_2_genes = parent_2_gene_sequence[start_gene_index : end_gene_index]
            if parent_1_gene_sequence[0] in parent_2_genes:
                parent_2_genes.remove(parent_1_gene_sequence[0])

            # Create the child gene sequence with only the first parents genes
            child_gene_sequence = [gene for gene in parent_1_gene_sequence if gene not in parent_2_genes]

            # Insert the parent 2 genes into the child gene sequence at the correct positions
            for position, element in enumerate(parent_2_genes, start_gene_index):
                child_gene_sequence.insert(position, element)

            # Make sure the last city is the same as the beginning city
            if len(child_gene_sequence) != 0:
                child_gene_sequence[-1] = child_gene_sequence[0]  
            
            # Create an individual based on the child's gene sequence
            children.append(Individual(gene_pool=self.gene_pool, gene_sequence=child_gene_sequence))

        # Make the best parents and their children the next generation
        best_individuals += children + extra_population
      
        return best_individuals


    def mutate(self, mutation_rate):
        """
        Mutate the population if a randomly generated number is less than the mutation rate
        """
        if random.random() < mutation_rate:
            population = self.get_population()
            for individual in population:
                individual.mutate(mutation_rate)


def create_plot(generations, fitness_counts):
    """
    Graphs the average fitness score for every generation
    """
    print(generations)
    print(fitness_counts)
    plt.plot(generations, fitness_counts, color='lightblue', linewidth=3)
    plt.title('Fitness Score per Generation')
    plt.xlabel('Generation')
    plt.ylabel('Fitness Score')
    plt.grid(True)
    plt.show()

