import time
from utilityFunctions import City, Individual, Population, create_gene_pool, create_plot


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
    AMOUNT_OF_GENERATIONS = 50
    SIZE_OF_POPULATION = 500
    MUTATION_RATE = 0.2

    start = time.monotonic()
    # Create gene pool and beginning population
    gene_pool = create_gene_pool()
    population = Population(gene_pool=gene_pool, size_of_population=SIZE_OF_POPULATION)

    generation = []
    fitness_counts = []

    generation_count = 0
    # while population.size_of_population > 1:
    while generation_count <= AMOUNT_OF_GENERATIONS:
        # Get all the individuals in the population
        generation.append(generation_count)
        individuals = population.get_population()
        
        # Calculate the average for the population in order to graph
        fitness_counts.append(average_fitness(individuals))
        
        #Create the next generation by mating the best half of the parent population and keeping the best parents
        print('mating', generation_count)
        next_generation = population.mate() 
        print('done')
        
        # Create a new population as the next generation and apply mutation to them
        population = Population(gene_pool=gene_pool, individuals=next_generation)
        population.mutate(MUTATION_RATE)

        # Increment generation
        generation_count += 1

    print(time.monotonic() - start)
    
    # Plot the average fitness score per generation
    create_plot(generation, fitness_counts)    

if __name__ == '__main__':
    main()
