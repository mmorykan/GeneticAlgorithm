import celery
import numpy
import random
from utilityFunctions import Individual, City

app = celery.Celery('genetics')
app.config_from_object('config')


@app.task
def get_fitness_scores(individuals):
    return individuals.get_fitness()


@app.task(serializer='pickle')
def mating(all_parents, gene_pool):
    children = []
    for i in range(0, len(all_parents), 2):
        parent_1 = all_parents[i]
        parent_2 = all_parents[i + 1]

        parent_1_gene_sequence = parent_1.get_gene_sequence()
        parent_2_gene_sequence = parent_2.get_gene_sequence()


        child_gene_sequence = []
        for i in range(0, len(parent_1_gene_sequence), 2):
            city_1 = parent_1_gene_sequence[i]
            city_2 = parent_2_gene_sequence[i]

            next_city_1 = parent_1_gene_sequence[i + 1]
            next_city_2 = parent_2_gene_sequence[i + 1]

            city_1_to_next = gene_pool[city_1].get_distance(gene_pool[next_city_1])
            city_2_to_next = gene_pool[city_2].get_distance(gene_pool[next_city_2])

            if city_1_to_next < city_2_to_next:
                child_gene_sequence.extend([city_1, next_city_1])
            else:
                child_gene_sequence.extend([city_2, next_city_2])

            child_gene_sequence[-1] = child_gene_sequence[0]
        
        children.append(child_gene_sequence)

    return children

app.conf.task_serializer = 'pickle'

