"""
We will be using a genetic algorithm to solve the knapsack problem! 
The Knapsack Problem is a classic optimization challenge: given items 
with weights and values, select a subset to maximize total value within a 
fixed weight capacity, deciding whether to take an item or leave it (0/1) 
or take fractions (Fractional Knapsack)
"""

import time
from typing import Callable, List, Tuple
from random import * 
from collections import namedtuple
from functools import partial



Genome = List[int] # induviduals, represented as lists of 0s and 1s
Population = List[Genome] # one population is a list of genomes!
Thing = namedtuple("Thing", ["name", "value", "weight"]) # Thing(value, weight)
PopulateFunc = Callable[[Genome], int]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
FitnessFunc = Callable[[Genome], int] # a function that takes a genome and returns an int (fitness score)
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]

things = [
    Thing('Laptop',value=500, weight=2200), 
    Thing('Headphones', value=150, weight=160),
    Thing('Coffee Mug', value=60, weight=350),
    Thing('Notepad', value=40, weight=333),
    Thing('Water Bottle', value=30, weight=192),
    ]

def generate_genome(length: int) -> Genome: 
    # generates a random genome made of 0s and 1s, and a given length
    return choices([0, 1], k=length)


def generate_population(size: int, genome_length: int) -> Population:
    # generates a population of given size, each genome having the given length
    return [generate_genome(genome_length) for _ in range(size)]

def fitness(genome: Genome, things: List[Thing], weight_limit: int) -> int:
    # calculates the fitness of a genome based on the things and weight limit
    if len(genome) != len(things):
        raise ValueError("Genome length and number of things must be the same")
    weight = 0 
    value = 0 

    for i, thing in enumerate(things): 
        # a genetic sequence will determine whether we include a thing or not! 
        if genome[i] == 1: # if the gene is 1, we include the thing
            weight += thing.weight
            value += thing.value
            if weight > weight_limit: # if we exceed the weight limit, return 0
                return 0
    return value

def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
   # randomly select two genomes, with the fitter genomes having a higher chance of being choosen (aka, parents for crossover)
    return choices(
        population=population,
        weights=[fitness_func(genome) for genome in population],# build a list of fitness scores for each genome
        k=2 
    )  

def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]: 
    if len(a) != len(b):
        raise ValueError("Genomes a and b must be of the same length")
    
    length = len(a)
    if length < 2:
        return a, b  # no crossover possible if genome is too short
    
    p = randint(1, length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]  

def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num): 
        index = randrange(len(genome))
        genome[index] = genome[index] if random() > probability else abs(genome[index] -1)
    return genome


def run_evolution(
    populate_func: PopulateFunc,
    fitness_func: FitnessFunc,
    fitness_limit: int,
    selection_func: SelectionFunc = selection_pair,
    crossover_func: CrossoverFunc = single_point_crossover,
    mutation_func: MutationFunc = mutation,
    generation_limit: int = 100,
) -> Tuple[Population, int]:

    population = populate_func()

    for generation in range(generation_limit):

        population = sorted(
            population,
            key=lambda genome: fitness_func(genome),
            reverse=True
        )

        if fitness_func(population[0]) >= fitness_limit:
            break

        next_generation = population[0:2]  # elitism

        for _ in range(int(len(population) / 2) - 1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            next_generation.append(mutation_func(offspring_a))
            next_generation.append(mutation_func(offspring_b))

        population = next_generation

    return population, generation


start = time.time()
population, generations = run_evolution(
    population_func = partial(
        generate_population, size=10, genome_length=len(things)
    ), 
    fitness_func=partial(
        fitness, things=things,weight_limit=3000
    ),
    fitness_limit=740, 
    generation_limit=100
)

end = time.time()

def genome_to_things(genome: Genome, things: [Thing]) -> [Thing]: 
    result = []
    for i, thing in enumerate(things): 
        if genome[i] == 1: 
            result += [thing.name]
    return result

print(f"number of generations: {generations}")
print(f"time: {end - start} seconds")
print(f"best solution: {genome_to_things(population[0], things)}")

        