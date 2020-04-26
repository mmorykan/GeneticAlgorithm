import random
import numpy


def create_gene_pool():
    """
    Create a fixed amount of genes that one animal can have
    Assigns random coordinates to each city created
    """
    genes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '[', 
            ']', '{', '}', '|', ';', '<', '>', '/', '?']
    gene_pool = {}
    for gene in genes:
        gene_pool[gene] = City(random.randint(0, 10000), random.randint(0, 10000))

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
    Creates a population from only a gene pool and specified size or from a list of individuals
    Gets fitness scores and calculates the individuals with the best fitness scores
    Can make the individuals with the best fitness scores mate and products children individuals
    """
    def __init__(self, gene_pool=None, size_of_population=10, individuals=None):
        self.gene_pool = gene_pool
        self.size_of_population = size_of_population
        if individuals:
            self.individuals = individuals
        else:
            self.individuals = [Individual(gene_pool=self.gene_pool) for _ in range(self.size_of_population)]


    def get_population(self):
        return self.individuals


    def get_fitness_scores(self):
        fitness_scores = {}
        for individual in self.individuals:
            fitness_score = individual.get_fitness()
            fitness_scores[individual] = fitness_score
        
        return fitness_scores


    def get_best_fitness_individuals(self):
        fitness_scores = self.get_fitness_scores()
        best_individuals = []

        halve_population = len(fitness_scores) // 2
        if halve_population % 2 == 1:
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
        children = []
        for i in range(0, len(all_parents), 2):
            # print(i)
            parent_1 = all_parents[i]
            parent_2 = all_parents[i + 1]

            parent_1_gene_sequence = parent_1.get_gene_sequence()
            parent_2_gene_sequence = parent_2.get_gene_sequence()

            start_gene_index = random.randint(0, len(parent_2_gene_sequence) - 4)
            end_gene_index = random.randint(start_gene_index + 1, len(parent_2_gene_sequence))

            parent_2_genes = parent_2_gene_sequence[start_gene_index : end_gene_index]
            child_gene_sequence = [gene for gene in parent_1_gene_sequence if gene not in parent_2_genes]

            for position in range(start_gene_index, end_gene_index):
                child_gene_sequence.insert(position, parent_2_gene_sequence[position])
            
            # print(child_gene_sequence)
            children.append(Individual(gene_pool=self.gene_pool, gene_sequence=child_gene_sequence))

        return children


def main():
    gene_pool = create_gene_pool()
    population = Population(gene_pool=gene_pool, size_of_population=1000)

    while population.size_of_population > 1:
        next_generation = population.get_best_fitness_individuals()
        next_generation = Population(gene_pool=gene_pool, size_of_population=len(next_generation), individuals=next_generation)
        children = next_generation.mate()

        for i in children:
            print(i.get_fitness())

        population = Population(gene_pool=gene_pool, size_of_population=len(children), individuals=children)


    # next_generation = population.get_best_fitness_individuals()
    # for i in next_generation:
    #     print(i)
    #     print(i.get_fitness())
    # next_generation = Population(gene_pool=gene_pool, individuals=next_generation)
    # print(next_generation)
    # children = next_generation.mate()
    # for i in children:
    #     print(i)
    #     print(i.get_fitness())
    
    

if __name__ == '__main__':
    main()
