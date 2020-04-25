import random
import numpy


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
    def __init__(self, gene_pool):
        self.gene_pool = gene_pool
        

    def create_gene_sequence(self):
        """
        Creates one individual by randomly taking a sample from the gene pool and adding the home city on the end
        """
        gene_sequence = random.sample(list(self.gene_pool), len(self.gene_pool))
        gene_sequence += gene_sequence[0]
        return gene_sequence


    def determine_fitness(self):
        total_distance = 0
        gene_sequence = self.get_gene_sequence()
        for gene in range(len(gene_sequence)):
            if gene == len(gene_sequence) - 1:
                break
            city_1 = self.gene_pool[gene_sequence[gene]]
            print(city_1.x_coord, city_1.y_coord)
            city_2 = self.gene_pool[gene_sequence[gene + 1]]
            print(city_2.x_coord, city_2.y_coord)
            total_distance += city_1.get_distance(city_2)

        return total_distance


    def get_gene_sequence(self):
        return self.create_gene_sequence()


    def get_fitness(self):
        return self.determine_fitness()
    

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


def main():
    gene_pool = create_gene_pool()
    first_individual = Individual(gene_pool)
    sequence = first_individual.create_gene_sequence()
    fitness = first_individual.get_fitness()
    print(sequence)
    print(fitness)



if __name__ == '__main__':
    main()