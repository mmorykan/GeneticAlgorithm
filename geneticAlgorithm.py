import random
import numpy


class city:
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
        gene_pool[gene] = city(random.randint(0, 10000), random.randint(0, 10000))

    return gene_pool


def create_gene_sequence(gene_pool):
    """
    Creates one individual by randomly taking a sample from the gene pool and adding the home city on the end
    """
    gene_sequence = random.sample(list(gene_pool), len(gene_pool))
    gene_sequence += gene_sequence[0]
    return gene_sequence


def main():
    gene_pool = create_gene_pool()
    gene_sequence = create_gene_sequence(gene_pool)
    print(gene_sequence)

if __name__ == '__main__':
    main()