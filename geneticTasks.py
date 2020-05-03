import celery
import numpy
import random
from utilityFunctions import Individual, City

app = celery.Celery('genetics')
app.config_from_object('config')


@app.task
def get_fitness_scores(individuals):
    """
    Return a list of fitness scores for every individual in the population
    """
    return individuals.get_fitness()


@app.task
def mating(best_individuals, gene_pool):
    """
    Mate the best individuals from a population using apply_async celery function
    Returns a list of child gene sequences
    """
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
        start_gene_index = random.randint(0, len(parent_2_gene_sequence) - 2)
        end_gene_index = random.randint(start_gene_index + 1, len(parent_2_gene_sequence))

        # Get the correct genes from parent 2 
        parent_2_genes = parent_2_gene_sequence[start_gene_index : end_gene_index]
        if parent_1_gene_sequence[0] in parent_2_genes:
            parent_2_genes.remove(parent_1_gene_sequence[0])

        # Create the child gene sequence with only the first parents genes
        child_gene_sequence = [gene for gene in parent_1_gene_sequence if gene not in parent_2_genes]

        # Insert the parent 2 genes into the child gene sequence at the correct positions
        for position, element in enumerate(parent_2_genes, start_gene_index):
            child_gene_sequence.insert(position, parent_2_gene_sequence[position])        

        # Make sure the last city is the same as the beginning city
        if len(child_gene_sequence) != 0:
            child_gene_sequence[-1] = child_gene_sequence[0]  
            
        
        children.append(child_gene_sequence)

    return children


@app.task
def get_best_fitness(fitness_scores):
    """
    Find the best half of the fitness scores from the fitness scores of the whole population
    Return a list of the gene sequences with those fitness scores
    """
    best_individuals = []

    halve_population = len(fitness_scores) // 2 
    if halve_population % 2 == 1:  # Need to make the half of the population even in order for everyone to be able to mate
        halve_population -= 1

    for _ in range(halve_population):
        for individual, score in fitness_scores.items():
            if score == min(fitness_scores.values()):  # Find the individual with the best fitness score
                best_individuals.append(individual.get_gene_sequence())
                fitness_scores[individual] = max(fitness_scores.values())   # Set the individual with best score to highest score
                break

    return best_individuals


app.conf.task_serializer = 'pickle'  # Use pickle for all tasks instead of the default JSON

