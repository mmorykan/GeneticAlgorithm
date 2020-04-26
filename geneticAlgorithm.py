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
        gene_pool[gene] = City(random.randint(0, 200), random.randint(0, 200))

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
    def __init__(self, gene_pool=None, gene_sequence=None):
        self.gene_pool = gene_pool
        if gene_sequence:
            self.gene_sequence = gene_sequence
        else:
            self.gene_sequence = self.create_gene_sequence()
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
        for gene in range(len(gene_sequence)):
            if gene == len(gene_sequence) - 1:
                break
            city_1 = self.gene_pool[gene_sequence[gene]]
            city_2 = self.gene_pool[gene_sequence[gene + 1]]
            total_distance += city_1.get_distance(city_2)

        self.fitness = total_distance

        return total_distance


    def get_gene_sequence(self):
        return self.gene_sequence


    def get_fitness(self):
        return self.fitness
    

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
        all_parents = self.get_best_fitness_individuals()
        # all_parents = self.individuals
        children = []

        for i in range(0, len(all_parents), 2):
            parent_1 = all_parents[i]
            parent_2 = all_parents[i + 1]

            parent_1_gene_sequence = parent_1.get_gene_sequence()
            parent_2_gene_sequence = parent_2.get_gene_sequence()

            # Mating algorithm 1: not working well

            # start_gene_index = random.randint(0, len(parent_2_gene_sequence) - 4)
            # end_gene_index = random.randint(start_gene_index + 1, len(parent_2_gene_sequence))

            # parent_2_genes = parent_2_gene_sequence[start_gene_index : end_gene_index]
            # child_gene_sequence = [gene for gene in parent_1_gene_sequence if gene not in parent_2_genes]

            # for position in range(start_gene_index, end_gene_index):
            #     child_gene_sequence.insert(position, parent_2_gene_sequence[position])

            # Mating algorithm 2: Not working well

            # child_gene_sequence = parent_1_gene_sequence[:len(parent_1_gene_sequence) // 2] + parent_2_gene_sequence[len(parent_2_gene_sequence) // 2:]

            # Mating algorithm 3: Very greedy algorithm. Probably as good as we are going to get

            child_gene_sequence = []
            for i in range(0, len(parent_1_gene_sequence), 2):
                city_1 = parent_1_gene_sequence[i]
                city_2 = parent_2_gene_sequence[i]

                next_city_1 = parent_1_gene_sequence[i + 1]
                next_city_2 = parent_2_gene_sequence[i + 1]

                city_1_to_next = self.gene_pool[city_1].get_distance(self.gene_pool[next_city_1])
                city_2_to_next = self.gene_pool[city_2].get_distance(self.gene_pool[next_city_2])

                if city_1_to_next < city_2_to_next:
                    child_gene_sequence.extend([city_1, next_city_1])
                else:
                    child_gene_sequence.extend([city_2, next_city_2])
            
            children.append(Individual(gene_pool=self.gene_pool, gene_sequence=child_gene_sequence))

        return children


def create_plot(generations, fitness_counts):
    print(generations)
    print(fitness_counts)
    plt.plot(generations, fitness_counts, color='lightblue', linewidth=3)
    plt.title('Fitness score per generation')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.show()


def main():
    gene_pool = create_gene_pool()
    population = Population(gene_pool=gene_pool, size_of_population=100)

    generation = []
    fitness_counts = []

    generation_count = 0
    while population.size_of_population > 1:

        children = population.mate()
        print(len(children))
        if len(children) == 0:
            break

        fitness_num = 0
        for child in children:
            fitness = child.get_fitness()
            fitness_num += fitness
            print(fitness)
            
        fitness_counts.append(fitness_num / len(children))


        population = Population(gene_pool=gene_pool, individuals=children)

        generation.append(generation_count)
        generation_count += 1

    create_plot(generation, fitness_counts)    

if __name__ == '__main__':
    main()
