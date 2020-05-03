import random
import numpy
import time
from matplotlib import pyplot as plt
from utilityFunctions import City, Individual


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


# class City:
#     """
#     Creates the city as a pair of x and y coordiantes.
#     Can calculate the distance between two cities
#     """
#     def __init__(self, x_coord, y_coord):
#         self.x_coord = x_coord
#         self.y_coord = y_coord


#     def get_distance(self, city):
#         x_distance = abs(self.x_coord - city.x_coord)
#         y_distance = abs(self.y_coord - city.y_coord)
#         return numpy.sqrt(x_distance**2 + y_distance**2)

        
# class Individual:
#     """
#     Creates an individual by creating its own gene sequence
#     Calculates the fitness quality of an individual
#     """
#     def __init__(self, gene_pool=None, gene_sequence=None):
#         self.gene_pool = gene_pool
#         if gene_sequence:
#             self.gene_sequence = gene_sequence
#         else:
#             self.gene_sequence = self.create_gene_sequence()
#         self.fitness = self.determine_fitness()  # Distribute this step
        

#     def create_gene_sequence(self):
#         """
#         Creates one individual by randomly taking a sample from the gene pool and adding the home city on the end
#         """
#         gene_sequence = random.sample(list(self.gene_pool), len(self.gene_pool))
#         gene_sequence += gene_sequence[0]
#         self.gene_sequence = gene_sequence
#         return gene_sequence


#     def determine_fitness(self):
#         """
#         Calculate the distance between each city. The total distance is the fitness value
#         """
#         total_distance = 0
#         gene_sequence = self.get_gene_sequence()
#         for gene in range(len(gene_sequence) - 1):
#             city_1 = self.gene_pool[gene_sequence[gene]]
#             city_2 = self.gene_pool[gene_sequence[gene + 1]]
#             total_distance += city_1.get_distance(city_2)

#         self.fitness = total_distance

#         return total_distance


#     def get_gene_sequence(self):
#         return self.gene_sequence


#     def get_fitness(self):
#         return self.fitness
    

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


    def get_fitness_scores(self):
        """
        Return a dictionary of individuals and fitness scores
        """
        fitness_scores = {}
        for individual in self.individuals:
            fitness_score = individual.get_fitness()
            fitness_scores[individual] = fitness_score
        
        return fitness_scores


    def get_best_fitness_individuals(self):
        """
        Return the half of individuals with the best fitness scores
        """
        fitness_scores = self.get_fitness_scores()
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

        return best_individuals


    def mate(self):
        """
        Gets the best individuals from the population 
        Takes a random subset of the second parents gene sequence and copies it directly into a copy of the 
        first parents gene sequence at the same positions. This is the new child gene sequence
        Creates a new individual instance for every child
        """
        best_individuals = self.get_best_fitness_individuals()
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
            start_gene_index = random.randint(0, 60)
            end_gene_index = random.randint(start_gene_index + 1, 62)
            print('\n', start_gene_index, '\n', end_gene_index)

            # Get the correct genes from parent 2 
            parent_2_genes = parent_2_gene_sequence[start_gene_index : end_gene_index]
            if parent_1_gene_sequence[0] in parent_2_genes:
                parent_2_genes.remove(parent_1_gene_sequence[0])

            # Create the child gene sequence with only the first parents genes
            child_gene_sequence = [gene for gene in parent_1_gene_sequence if gene not in parent_2_genes]
            child_gene_sequence += [0] * len(parent_2_genes)

            # Insert the parent 2 genes into the child gene sequence at the correct positions
            for position in range(start_gene_index, end_gene_index):
                child_gene_sequence.insert(position, parent_2_gene_sequence[position])

            del child_gene_sequence[-len(parent_2_genes):]
            

            # Make sure the last city is the same as the beginning city
            if len(child_gene_sequence) != 0:
                child_gene_sequence[-1] = child_gene_sequence[0]  
            
            # Create an individual based on the child's gene sequence
            children.append(Individual(gene_pool=self.gene_pool, gene_sequence=child_gene_sequence))

        # Make the best parents and their children the next generation
        best_individuals += children

        return best_individuals


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


def average_fitness(individuals):
    """
    Calculate the average fitness score for a generation
    """
    fitness_num = 0
    for individual in individuals:
        fitness = individual.get_fitness()
        fitness_num += fitness
    return fitness_num / len(individuals)


def main():
    start = time.monotonic()
    # Create gene pool and beginning population
    gene_pool = create_gene_pool()
    population = Population(gene_pool=gene_pool, size_of_population=1000)

    generation = []
    fitness_counts = []

    generation_count = 0
    while population.size_of_population > 1:
        # Get all the individuals in the population
        generation.append(generation_count)
        individuals = population.get_population()
        
        # Calculate the average for the population in order to graph
        fitness_counts.append(average_fitness(individuals))

        #Create the next generation by mating the best half of the parent population and keeping the best parents
        next_generation = population.mate() 
        if len(next_generation) == 0:
            break
        population = Population(gene_pool=gene_pool, individuals=next_generation)


        # Increment generation
        generation_count += 1

    print(time.monotonic() - start)
    # Plot the average fitness score per generation
    create_plot(generation, fitness_counts)    

if __name__ == '__main__':
    main()
