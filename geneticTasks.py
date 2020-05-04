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
def mating(parent_1, parent_2):
    """
    Mate the best individuals from a population using apply_async celery function
    Returns a list of child gene sequences
    """
    # children = []

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
        child_gene_sequence.insert(position, parent_2_gene_sequence[position])        

    # Make sure the last city is the same as the beginning city
    if len(child_gene_sequence) != 0:
        child_gene_sequence[-1] = child_gene_sequence[0]  
        
    
    # children.append(child_gene_sequence)

    return child_gene_sequence


app.conf.task_serializer = 'pickle'  # Use pickle for all tasks instead of the default JSON

